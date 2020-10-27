import pandas as pd
import geopandas
from read_shapeFile import loadShapeFile
import numpy as np
import time
import argparse
from NDVI_sent import NDVI_img, calc_NDVI_census
from calc_greenSpacesProximityIndex import prox_Ind, proxToCensal

def arg_parse():
    parser = argparse.ArgumentParser(description='Data division so make 2 class into 1 class')

    # Datasets parameters
    parser.add_argument('--merge_green_spaces', type=int, default=0,
                    help="1 if you need to merge green spaces into file, 0 if file is already merged.")
    parser.add_argument('--merge_build_spaces', type=int, default=0,
                        help="1 if you need to merge build spaces into file, 0 if file is already merged.")
    parser.add_argument('--NDVI_img_out', type=str, default='out/ndviImage.tiff',
                        help="String containing the location to store the NDVI image file")
    parser.add_argument('--sent_B04', type=str, default='data/sentinel/sent_B04.jp2',
                        help="String containing the location to the sentinel2 image in the B04 band.")
    parser.add_argument('--sent_B08', type=str, default='data/sentinel/sent_B08.jp2',
                        help="String containing the location to the sentinel2 image in the B08 band.")
    args = parser.parse_args()
    return args

def indexes_calc(census_inhabitants, greenSpaces, buildSpaces):
    # Crete arrays for the different calculated index
    greenSpaceIndex = []
    greenSpaceDensity = []
    greenSpaceBuiltSpaceRatio = []
    tic = time.clock()

    # Loop to calcaulate the different indexes for each census area
    for i in range(len(census_inhabitants.index)):
        # Calcualte process time
        if ((i + 1) % 100 == 0):
            toc = time.clock()
            print('Done with ' + str(i + 1) + '/' + str(
                len(census_inhabitants.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = time.clock()

        seccionesCensal_polygon = census_inhabitants['geometry'][i]
        green_space = 0
        built_space = 0

        # Calculate the area of green and build space for each census
        for greenSpaces_polygon in greenSpaces['geometry']:
            if greenSpaces_polygon.intersects(seccionesCensal_polygon):
                # green_space += seccionesCensal_polygon.intersection(greenSpaces_polygon).area
                green_space += greenSpaces_polygon.area

        for buildSpaces_polygon in buildSpaces['geometry']:
            if buildSpaces_polygon.intersects(seccionesCensal_polygon):
                # built_space += seccionesCensal_polygon.intersection(buildSpaces_polygon).area
                built_space += buildSpaces_polygon.area

        # Make the calculations for each index, if there is any division by 0, 9999 will be added instead of the division
        try:
            greenSpaceIndex.append(green_space / census_inhabitants['Inhabitants'][i])
        except ZeroDivisionError:
            greenSpaceIndex.append(9999)

        try:
            greenSpaceDensity.append(green_space / seccionesCensal_polygon.area)
        except ZeroDivisionError:
            greenSpaceDensity.append(9999)

        try:
            greenSpaceBuiltSpaceRatio.append(green_space / built_space)
        except ZeroDivisionError:
            greenSpaceBuiltSpaceRatio.append(9999)

    # Add new columns to the ShapeFile containing the new calculated index
    census_inhabitants['greenSpaceIndex'] = np.array(greenSpaceIndex)
    census_inhabitants['greenSpaceDensity'] = np.array(greenSpaceDensity)
    census_inhabitants['greenSpaceBuiltSpaceRatio'] = np.array(greenSpaceBuiltSpaceRatio)
    return census_inhabitants

if __name__ == '__main__':
    args = arg_parse()
    # Open censo xls file and remove unwanted rows
    columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
    census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names=columns, header=8, index_col=0)
    census.index = census.index.str.strip()
    census = census.iloc[:4417]
    census = census.groupby(census.index).sum()

    # Combine the census population data with the ShapeFile of seccionesCensales
    seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
    census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
    census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')

    if args.merge_green_spaces:
        # Load shapefiles of green and constructed areas
        urbanGardens_shp = loadShapeFile('data/Carto_1000/11_HUERTO_URBANO_P.shp')
        gardenAreas_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_P.shp')
        gardenInPatios_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')
        greenSpaces = pd.concat([urbanGardens_shp, gardenAreas_shp, gardenInPatios_shp])
        greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')

    greenSpaces = loadShapeFile('data/greenSpaces.shp')

    if args.merge_build_spaces:
        buildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_EN_CONSTRUCCION_P.shp')
        buildingsUnderConstruction_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_INDEFINIDO_P.shp')
        undefinedBuildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_P.shp')
        buildSpaces = pd.concat([buildings_shp, buildingsUnderConstruction_shp, undefinedBuildings_shp])
        buildSpaces.to_file('data/buildSpaces.shp', driver='ESRI Shapefile')

    buildSpaces = loadShapeFile('data/buildSpaces.shp')

    census_inhabitants = indexes_calc(census_inhabitants, greenSpaces, buildSpaces)
    greenSpaces = prox_Ind(greenSpaces)
    census_inhabitants = proxToCensal(greenSpaces, census_inhabitants)
    NDVI_img(args.sent_B04, args.sent_B08, args.NDVI_img_out)
    census_inhabitants = calc_NDVI_census(census_inhabitants, args.NDVI_img_out)

    # Save results into a new ShapeFile
    census_inhabitants = geopandas.GeoDataFrame(census_inhabitants, geometry='geometry')
    census_inhabitants.to_file('out/indexes.shp', driver='ESRI Shapefile')

    print('fin')

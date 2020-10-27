from rasterio import plot
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
from shapely.geometry import mapping
from read_shapeFile import loadShapeFile
import numpy as np
import time
from rasterio.mask import mask

def calc_NDVI_census(census_inhabitants, img_NDVI):
    ndvi = rasterio.open(img_NDVI)
    tic = time.clock()
    ndvi_census = []
    ndvi_var = []
    ndvi_min = []
    ndvi_max = []

    for i in range(len(census_inhabitants.index)):
        # Calcualte process time
        NDVI_calcs = []
        if ((i + 1) % 100 == 0):
            toc = time.clock()
            print('Done with ' + str(i + 1) + '/' + str(
                len(census_inhabitants.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = time.clock()

        NDVI_clipped, _ = rasterio.mask.mask(ndvi, [mapping(census_inhabitants['geometry'][i])], crop=True)
        for y in NDVI_clipped[0]:
            for x in y:
                if x != 0:
                    NDVI_calcs.append(x)

        avg = sum(NDVI_calcs) / len(NDVI_calcs)
        var = np.var(NDVI_calcs)
        min_NDVI = min(NDVI_calcs)
        max_NDVI = max(NDVI_calcs)
        ndvi_census.append(avg)
        ndvi_var.append(var)
        ndvi_min.append(min_NDVI)
        ndvi_max.append(max_NDVI)

    census_inhabitants['NDVI'] = np.array(ndvi_census)
    census_inhabitants['NDVI_var'] = np.array(ndvi_var)
    census_inhabitants['NDVI_min'] = np.array(ndvi_min)
    census_inhabitants['NDVI_max'] = np.array(ndvi_max)
    # Save results into a new ShapeFile
    print('Finished calculating NDVI')

    return census_inhabitants
    #census_inhabitants = geopandas.GeoDataFrame(census_inhabitants, geometry='geometry')
    #census_inhabitants.to_file('out/indexes_NDVI.shp', driver='ESRI Shapefile')

def NDVI_img(b4, b8, img_out):
    # Open each band using gdal
    band4 = rasterio.open(b4)
    band8 = rasterio.open(b8)

    # read in each band as array and convert to float for calculations
    #raster sytem of reference
    print(band4.crs)

    #multiple band representation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    plot.show(band4, ax=ax1, cmap='Blues') #red
    plot.show(band8, ax=ax2, cmap='Blues') #nir
    fig.tight_layout()

    #generate nir and red objects as arrays in float64 format
    red = band4.read(1).astype('float64')
    nir = band8.read(1).astype('float64')

    #ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi=np.where(
        (nir+red)==0.,
        0,
        (nir-red)/(nir+red))


    #export ndvi image
    ndviImage = rasterio.open(img_out,'w',
                              driver='Gtiff',
                              width=band4.width,
                              height = band4.height,
                              count=1, crs=band4.crs,
                              transform=band4.transform,
                              dtype='float64')

    ndviImage.write(ndvi,1)
    ndviImage.close()

if __name__ == '__main__':
    # Load ShapeFiles of green areas and censal areas
    columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
    census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names=columns, header=8, index_col=0)
    census.index = census.index.str.strip()
    census = census.iloc[:4417]
    census = census.groupby(census.index).sum()

    # Combine the census population data with the ShapeFile of seccionesCensales
    seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
    census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
    census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')

    img_NDVI = 'out/ndviImage.tiff'
    b4 = 'data/sentinel/sent_B04.jp2'
    b8 = 'data/sentinel/sent_B08.jp2'

    NDVI_img(b4, b8, img_NDVI)
    calc_NDVI_census(census_inhabitants, img_NDVI)

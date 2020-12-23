import geopandas
from read_shapeFile import loadShapeFile
import argparse
from NDVI_sent import NDVI_img, calc_NDVI_section
from create_green_build_spaces import green_build_join
from calc_greenSpaceIndex import indexes_calc
from get_seccions import get_secciones_censales, get_barrios, get_distritos
from calc_greenSpacesProximityIndex import greenProxInd, proxToSection
from read_shapeFile import ShapeFileToJson


def arg_parse():
    parser = argparse.ArgumentParser(description='Data division so make 2 class into 1 class')

    # Project parameters
    parser.add_argument('--merge_green_spaces', type=int, default=0,
                        help="1 if you need to merge green spaces into file, 0 if file is already merged.")
    parser.add_argument('--merge_build_spaces', type=int, default=0,
                        help="1 if you need to merge build spaces into file, 0 if file is already merged.")
    parser.add_argument('--green_proximity', type=int, default=0,
                        help="1 if you need to calculate green space proximity index in greenspaces and save it.")
    parser.add_argument('--all_spaces', type=int, default=0,
                        help="1 to merge into 1 all the files from all the districts.")
    parser.add_argument('--get_census', type=int, default=0,
                        help="1 to do calculations for censal areas.")
    parser.add_argument('--get_barrios', type=int, default=0,
                        help="1 to do calculations for barrios.")
    parser.add_argument('--get_distritos', type=int, default=1,
                        help="1 to do calculations for districts.")
    parser.add_argument('--NDVI_img_out', type=str, default='out/ndviImage.tiff',
                        help="String containing the location to store the NDVI image file")
    parser.add_argument('--sent_B04', type=str, default='data/sentinel/sent_B04.jp2',
                        help="String containing the location to the sentinel2 image in the B04 band.")
    parser.add_argument('--sent_B08', type=str, default='data/sentinel/sent_B08.jp2',
                        help="String containing the location to the sentinel2 image in the B08 band.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # Load parser
    args = arg_parse()

    # Create GreenSpace and BuildSpace files including all files from all districts
    green_build_join(args.all_spaces, args.merge_green_spaces, args.merge_build_spaces)

    # Load newly created files
    buildSpaces = loadShapeFile('data/buildSpaces.shp')
    greenSpaces = loadShapeFile('data/greenSpaces.shp')

    # Create censal area shapeFile with inhabitant count
    census = get_secciones_censales()

    # If needed, calculate green Space Proximity Index for all green spaces and save it
    if args.green_proximity:
        greenSpaces = greenProxInd(greenSpaces)
        greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')

    # Calculate all indexes for the censal areas
    if args.get_census:
        print('Starting calculations for censal areas')
        #census = get_secciones_censales()
        census = indexes_calc(census, greenSpaces, buildSpaces)
        census = proxToSection(census, greenSpaces)
        NDVI_img(args.sent_B04, args.sent_B08, args.NDVI_img_out)
        census = calc_NDVI_section(census, args.NDVI_img_out)

        # Save results into a new ShapeFile
        census = geopandas.GeoDataFrame(census, geometry='geometry')
        census.to_file('out/indexesCensal.shp', driver='ESRI Shapefile')
        ShapeFileToJson('out/indexesCensal.shp')

    # Calculate all indexes for the barrios
    if args.get_barrios:
        print('Starting calculations for barrios')
        barrios = get_barrios()
        barrios = indexes_calc(barrios, greenSpaces, buildSpaces)
        barrios = proxToSection(barrios, greenSpaces)
        NDVI_img(args.sent_B04, args.sent_B08, args.NDVI_img_out)
        barrios = calc_NDVI_section(barrios, args.NDVI_img_out)

        # Save results into a new ShapeFile
        barrios = geopandas.GeoDataFrame(barrios, geometry='geometry')
        barrios.set_crs(epsg=25830, inplace=True)
        barrios.to_file('out/indexesBarrios.shp', driver='ESRI Shapefile')
        ShapeFileToJson('out/indexesBarrios.shp')

    # Calculate all indexes for the districts
    if args.get_distritos:
        print('Starting calculations for districts')
        distritos = get_distritos(census)
        distritos = indexes_calc(distritos, greenSpaces, buildSpaces)
        distritos = proxToSection(distritos, greenSpaces)
        NDVI_img(args.sent_B04, args.sent_B08, args.NDVI_img_out)
        distritos = calc_NDVI_section(distritos, args.NDVI_img_out)

        # Save results into a new ShapeFile
        distritos = geopandas.GeoDataFrame(distritos, geometry='geometry')
        distritos.to_file('out/indexesDistritos.shp', driver='ESRI Shapefile')
        ShapeFileToJson('out/indexesDistritos.shp')

    print('fin')

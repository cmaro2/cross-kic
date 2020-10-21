import geopandas as gpd
import os
import json
import matplotlib.pyplot as plt


def ShapeFileToJson(shapeFilepath):
    data = gpd.read_file(shapeFilepath)

    #transforms read data to lat and long from utm
    data_latlong = data.to_crs(epsg=4326)
    #stores the info in a json
    data_latlong.to_file(shapeFilepath[:shapeFilepath.rfind('.')] + '.json', driver='GeoJSON')


def loadGeojson(jsonpath):
    if not(os.path.exists(jsonpath)):
        ShapeFileToJson(jsonpath[:jsonpath.rfind('.')] + '.shp')
    with open(jsonpath) as f:
        return json.load(f)

def loadShapeFile(shpfilePath, changeToCoord = False):
    if not(os.path.exists(shpfilePath)):
        print("File, " + shpfilePath + "does not exist")
        exit(-1)
    data = gpd.read_file(shpfilePath)
    #transforms read data to lat and long from utm
    if changeToCoord:
        return data.to_crs('epsg:4326')
    else:
        return data




if __name__ == '__main__':
    ShapeFileToJson('out/indexes.shp')

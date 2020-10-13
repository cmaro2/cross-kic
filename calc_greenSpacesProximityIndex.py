import pandas as pd
import geopandas
from read_shapeFile import loadShapeFile

# Load ShapeFiles of green areas
urbanGardens_shp = loadShapeFile('data/Carto_1000/11_HUERTO_URBANO_P.shp')
gardenAreas_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_P.shp')
gardenInPatios_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')

# Crete arrays for the different calculated index
urbanGardens_index = []
gardenAreas_index = []
gardenInPatios_index = []

# Minimum distance to which other green areas are checked
min_prox_dist = 200

print('Starting Urban Gardens')
for garden in urbanGardens_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) <= min_prox_dist):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) <= min_prox_dist):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) <= min_prox_dist):
            distance = garden.distance(gardenInPatio_polygon)

    if distance == 10000:
        prox = 0
    else:
        try:
            prox = garden.area/(distance * distance)
        except ZeroDivisionError:
            prox = garden.area
    urbanGardens_index.append(prox)

print('Starting Garden Areas')
for garden in gardenAreas_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) <= min_prox_dist):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) <= min_prox_dist):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) <= min_prox_dist):
            distance = garden.distance(gardenInPatio_polygon)

    if distance == 10000:
        prox = 0
    else:
        try:
            prox = garden.area/(distance * distance)
        except ZeroDivisionError:
            prox = garden.area
    gardenAreas_index.append(prox)

print('Starting Garden in Patios')
for garden in gardenInPatios_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) <= min_prox_dist):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) <= min_prox_dist):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) <= min_prox_dist):
            distance = garden.distance(gardenInPatio_polygon)

    if distance == 10000:
        prox = 0
    else:
        try:
            prox = garden.area/(distance * distance)
        except ZeroDivisionError:
            prox = garden.area
    gardenInPatios_index.append(prox)

print('Saving files')

# Convert files to geoPandas GeoDataFrame and save them
urbanGardens_shp = geopandas.GeoDataFrame(urbanGardens_shp, geometry='geometry')
gardenAreas_shp = geopandas.GeoDataFrame(gardenAreas_shp, geometry='geometry')
gardenInPatios_shp = geopandas.GeoDataFrame(gardenInPatios_shp, geometry='geometry')

urbanGardens_shp.to_file('out/urbanGardens.shp', driver='ESRI Shapefile')
gardenAreas_shp.to_file('out/gardenAreas.shp', driver='ESRI Shapefile')
gardenInPatios_shp.to_file('out/gardenInPatios.shp', driver='ESRI Shapefile')

print('Done')

import pandas as pd
from read_shapeFile import loadShapeFile
import numpy as np
import time

columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names = columns, header = 8, index_col=0)
census.index = census.index.str.strip()
census = census.groupby(census.index).sum()

seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')
urbanGardens_shp = loadShapeFile('data/Carto_1000/11_HUERTO_URBANO_P.shp')
gardenAreas_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_P.shp')
gardenInPatios_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')

urbanGardens_index = []
gardenAreas_index = []
gardenInPatios_index = []

print('Starting Urban Gardens')
for garden in urbanGardens_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) != 0):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) != 0):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) != 0):
            distance = garden.distance(gardenInPatio_polygon)

    prox = garden.area/(distance * distance)
    urbanGardens_index.append(prox)

print('Starting Garden Areas')
for garden in gardenAreas_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) != 0):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) != 0):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) != 0):
            distance = garden.distance(gardenInPatio_polygon)

    prox = garden.area/(distance * distance)
    gardenAreas_index.append(prox)

print('Starting Garden in Patios')
for garden in gardenInPatios_shp['geometry']:
    distance = 10000

    for urbanGarden_polygon in urbanGardens_shp['geometry']:
        if (garden.distance(urbanGarden_polygon) < distance) and (garden.distance(urbanGarden_polygon) != 0):
            distance = garden.distance(urbanGarden_polygon)

    for idx, gardenArea_polygon in enumerate(gardenAreas_shp['geometry']):
        if idx != 72:
            if (garden.distance(gardenArea_polygon) < distance) and (garden.distance(gardenArea_polygon) != 0):
                distance = garden.distance(gardenArea_polygon)

    for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
        if (garden.distance(gardenInPatio_polygon) < distance) and (garden.distance(gardenInPatio_polygon) != 0):
            distance = garden.distance(gardenInPatio_polygon)

    prox = garden.area / (distance * distance)
    urbanGardens_index.append(prox)

print('Done')

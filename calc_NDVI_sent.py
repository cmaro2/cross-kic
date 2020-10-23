import pandas as pd
import geopandas
import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import mapping
from read_shapeFile import loadShapeFile
import numpy as np
import time
import argparse
from rasterio import plot
from rasterio.mask import mask

columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names=columns, header=8, index_col=0)
census.index = census.index.str.strip()
census = census.iloc[:4417]
census = census.groupby(census.index).sum()

# Combine the census population data with the ShapeFile of seccionesCensales
seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')

ndvi = rasterio.open('out/ndviImage.tiff')
tic = time.clock()
ndvi_census = []

for i in range(len(census_inhabitants.index)):
    # Calcualte process time
    cnt = 0
    sum = 0
    if ((i + 1) % 100 == 0):
        toc = time.clock()
        print('Done with ' + str(i + 1) + '/' + str(
            len(census_inhabitants.index)) + ' census. Time in this cicle: ' + str(toc - tic))
        tic = time.clock()

    NDVI_clipped, _ = rasterio.mask.mask(ndvi, [mapping(census_inhabitants['geometry'][i])], crop=True)
    for y in NDVI_clipped[0]:
        for x in y:
            if x != 0:
                sum += x
                cnt += 1

    ndvi_census.append(sum/cnt)

census_inhabitants['NDVI'] = np.array(ndvi_census)
# Save results into a new ShapeFile
census_inhabitants = geopandas.GeoDataFrame(census_inhabitants, geometry='geometry')
census_inhabitants.to_file('out/indexes_NDVI.shp', driver='ESRI Shapefile')

print('fin')

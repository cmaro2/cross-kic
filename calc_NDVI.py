import pandas as pd
from read_shapeFile import loadShapeFile
import numpy as np

columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names = columns, header = 8, index_col=0)
census.index = census.index.str.strip()
census = census.groupby(census.index).sum()

seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')

census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')

aceras = loadShapeFile('data/NDVI/SHAPE_NDVI/EsAytMadridSCartSAT2018OtIndVegDifNDVISemestAnualTMnAcerasSphETRS89.shp')
parcelas = loadShapeFile('data/NDVI/SHAPE_NDVI/EsAytMadridSCartSAT2018OtIndVegDifNDVISemestAnualTMnParcelasSphETRS89.shp')
peatonal = loadShapeFile('data/NDVI/SHAPE_NDVI/EsAytMadridSCartSAT2018OtIndVegDifNDVISemestAnualTMnPeatonalSphETRS89.shp')
usos = loadShapeFile('data/NDVI/SHAPE_NDVI/EsAytMadridSCartSAT2018OtIndVegDifNDVISemestAnualTMnUsosSphETRS89.shp')

NVDI = []
for i in range(len(census_inhabitants.index)):
    seccionesCensal_polygon = census_inhabitants['geometry'][i]
    nvdi_area = 0
    area = 0

    for j in range(len(aceras.index)):
        if seccionesCensal_polygon.within(aceras['geometry'][j]):
            nvdi_area += aceras['NDVIOt18_M'][j] * aceras['geometry'][j].area
            area += aceras['geometry'][j].area

    for j in range(len(parcelas.index)):
        if seccionesCensal_polygon.within(parcelas['geometry'][j]):
            nvdi_area += parcelas['NDVIOt18_M'][j] * parcelas['geometry'][j].area
            area += parcelas['geometry'][j].area

    for j in range(len(peatonal.index)):
        if seccionesCensal_polygon.within(parcelas['geometry'][j]):
            nvdi_area += parcelas['NDVIOt18_M'][j] * parcelas['geometry'][j].area
            area += parcelas['geometry'][j].area

    for j in range(len(usos.index)):
        if seccionesCensal_polygon.within(usos['geometry'][j]):
            nvdi_area += usos['NDVIOt18_M'][j] * usos['geometry'][j].area
            area += usos['geometry'][j].area

    NVDI.append(nvdi_area/area)

seccionesCensales_shp['NVDI'] =  np.array(NVDI)

print('fin')

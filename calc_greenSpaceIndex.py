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
buildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_EN_CONSTRUCCION_P.shp')
buildingsUnderConstruction_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_INDEFINIDO_P.shp')
undefinedBuildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_P.shp')

greenSpaceIndex = []
greenSpaceDensity = []
greenSpaceBuiltSpaceRatio = []
tic = time.clock()
for i in range(len(census_inhabitants.index)):
       if((i+1)%100==0):
              toc = time.clock()
              print('Done with ' + str(i+1) + '/' + str(len(census_inhabitants.index)) + ' census. Time in this cicle: ' + str(toc-tic))
              tic = time.clock()
       seccionesCensal_polygon = census_inhabitants['geometry'][i]
       green_space = 0
       built_space = 0

       for urbanGarden_polygon in urbanGardens_shp['geometry']:
              if urbanGarden_polygon.intersects(seccionesCensal_polygon):
                     green_space += urbanGarden_polygon.intersection(seccionesCensal_polygon).area

       for idx, gardenArea_polygon in  enumerate(gardenAreas_shp['geometry']):
              if idx != 72:
                     if gardenArea_polygon.intersects(seccionesCensal_polygon):
                            green_space += gardenArea_polygon.intersection(seccionesCensal_polygon).area

       for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
              if gardenInPatio_polygon.intersects(seccionesCensal_polygon):
                     green_space += gardenInPatio_polygon.intersection(seccionesCensal_polygon).area

       for building_polygon in buildings_shp['geometry']:
              if building_polygon.intersects(seccionesCensal_polygon):
                     built_space += building_polygon.intersection(seccionesCensal_polygon).area

       for buildingUnderConstruction_polygon in buildingsUnderConstruction_shp['geometry']:
              if buildingUnderConstruction_polygon.intersects(seccionesCensal_polygon):
                     built_space += buildingUnderConstruction_polygon.intersection(seccionesCensal_polygon).area

       for undefinedBuilding_polygon in undefinedBuildings_shp['geometry']:
              if undefinedBuilding_polygon.intersects(seccionesCensal_polygon):
                     built_space += undefinedBuilding_polygon.intersection(seccionesCensal_polygon).area

       try:
              greenSpaceIndex.append(green_space/census_inhabitants['Inhabitants'][i])
       except ZeroDivisionError:
              greenSpaceIndex.append(9999)

       try:
              greenSpaceDensity.append(green_space/seccionesCensal_polygon.area)
       except ZeroDivisionError:
              greenSpaceDensity.append(9999)

       try:
              greenSpaceBuiltSpaceRatio.append(green_space/built_space)
       except ZeroDivisionError:
              greenSpaceBuiltSpaceRatio.append(9999)

census_inhabitants['greenSpaceIndex'] = np.array(greenSpaceIndex)
census_inhabitants['greenSpaceDensity'] = np.array(greenSpaceDensity)
census_inhabitants['greenSpaceBuiltSpaceRatio'] = np.array(greenSpaceBuiltSpaceRatio)

census_inhabitants.to_excel('out.xls')

print('fin')
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

urbanGardens_shp = loadShapeFile('Carto_1000/11_HUERTO_URBANO_P.shp')
gardenAreas_shp = loadShapeFile('Carto_1000/11_ZONA_AJARDINADA_P.shp')
gardenInPatios_shp = loadShapeFile('Carto_1000/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')
buildings_shp = loadShapeFile('Carto_1000/03_EDIFICIO_EN_CONSTRUCCION_P.shp')
buildingsUnderConstruction_shp = loadShapeFile('Carto_1000/03_EDIFICIO_INDEFINIDO_P.shp')
undefinedBuildings_shp = loadShapeFile('Carto_1000/03_EDIFICIO_P.shp')

greenSpaceIndex = []
greenSpaceDensity = []
greenSpaceBuiltSpaceRatio = []
for i in range(len(census_inhabitants.index)):
       #print(i)
       seccionesCensal_polygon = census_inhabitants['geometry'][i]
       green_space = 0
       built_space = 0

       for urbanGarden_polygon in urbanGardens_shp['geometry']:
              green_space += urbanGarden_polygon.intersection(seccionesCensal_polygon).area

       for j in range(len(gardenAreas_shp.index)):
       #TODO: when j = 72 the polygon is not valid
       #for gardenArea_polygon in gardenAreas_shp['geometry']:
              gardenArea_polygon = gardenAreas_shp['geometry'][j]
              #print(j)
              if j != 72:
                     green_space += gardenArea_polygon.intersection(seccionesCensal_polygon).area

       for gardenInPatio_polygon in gardenInPatios_shp['geometry']:
              green_space += gardenInPatio_polygon.intersection(seccionesCensal_polygon).area

       for building_polygon in buildings_shp['geometry']:
              built_space += building_polygon.intersection(seccionesCensal_polygon).area

       for buildingUnderConstruction_polygon in buildingsUnderConstruction_shp['geometry']:
              built_space += buildingUnderConstruction_polygon.intersection(seccionesCensal_polygon).area

       for undefinedBuilding_polygon in undefinedBuildings_shp['geometry']:
              built_space += undefinedBuilding_polygon.intersection(seccionesCensal_polygon).area

       greenSpaceIndex.append(green_space/census_inhabitants['Inhabitants'][i])
       greenSpaceDensity.append(green_space/seccionesCensal_polygon.area)
       greenSpaceBuiltSpaceRatio.append(green_space/built_space)

census_inhabitants['greenSpaceIndex'] = np.array(greenSpaceIndex)
census_inhabitants['greenSpaceDensity'] = np.array(greenSpaceDensity)
census_inhabitants['greenSpaceBuiltSpaceRatio'] = np.array(greenSpaceBuiltSpaceRatio)

print('fin')
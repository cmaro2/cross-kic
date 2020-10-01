import pandas as pd
from shape_file import loadShapeFile

columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
censo = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names = columns, header = 8, index_col=0)
censo.index = censo.index.str.strip()

seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')

map = {'0-4': 'niñxs', '5-9': 'niñxs', '10-14': 'niñxs',
       '15-19': 'jovenes', '20-24': 'jovenes',
       '25-29': 'adultos', '30-34': 'adultos', '35-39': 'adultos', '40-44': 'adultos',
       '45-49': 'adultos', '50-54': 'adultos', '55-59': 'adultos', '60-64': 'adultos',
       '65-69': 'ancianos', '70-74': 'ancianos', '75-79': 'ancianos', '80-84': 'ancianos',
       '85-89': 'ancianos', '90-94': 'ancianos', '95-99': 'ancianos', '100 y más': 'ancianos'}

censo_byAgeRange = censo.groupby(map, axis=1).sum()
fin = seccionesCensales_shp.join(censo_byAgeRange, on='CUSEC')

print('fin')
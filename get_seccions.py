import pandas as pd
from read_shapeFile import loadShapeFile
import numpy as np


def get_secciones_censales():
    columns = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls').loc[5]
    census = pd.read_excel('data/secciones_censales/2801_CensoMadrid2019.xls', names=columns, header=8, index_col=0)
    census.index = census.index.str.strip()
    census = census.iloc[:4417]
    census = census.groupby(census.index).sum()

    # Combine the census population data with the ShapeFile of seccionesCensales
    seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
    census_inhabitants = census.rename({'Total': 'Inhabitants'}, axis=1)['Inhabitants']
    census_inhabitants = seccionesCensales_shp.join(census_inhabitants, on='CUSEC')
    return census_inhabitants


def get_distritos():
    distritos = loadShapeFile('data/distritos/DISTRITOS_20200101_MADRID.shp')

    pob_file = pd.read_excel('data/distritos/dist_pob.xls', header=4, usecols=['Distrito', 'Total']).rename(
        columns={'Total': 'Inhabitants', 'Distrito': 'Name'})
    pob_file['Name'] = pob_file['Name'].str.capitalize()
    distritos = distritos.join(pob_file)

    return distritos


def get_barrios():
    barrios = loadShapeFile('data/barrios/barrios.shp')
    names_b = []
    for nom in barrios['DESBDT']:
        name = nom.split(' ', 1)[-1]
        names_b.append(name)

    barrios['Name'] = np.array(names_b)
    pob_file = pd.read_excel('data/barrios/barrios_pob.xls', header=4, usecols=['Total']).rename(
        columns={'Total': 'Inhabitants'})
    barrios = barrios.join(pob_file)
    barrios = barrios.drop(['DESBDT'], axis=1)

    return barrios

get_barrios()


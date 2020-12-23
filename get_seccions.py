import pandas as pd
from read_shapeFile import loadShapeFile
import numpy as np


# function to obtain shapefile with censal areas and their respective population count
def get_secciones_censales():
    census = pd.read_csv('data/CensoMadrid_2019.csv', sep=';', header=0).rename(columns={'Total': 'Inhabitants', 'Edad (grupos quinquenales)': 'Edad'})
    census = census.loc[census['Sexo']=='Ambos Sexos'].loc[census['Sección'] != 'TOTAL'].loc[census['Edad'] == 'Total']
    census = census.set_index('Sección')
    census['Inhabitants'] = pd.to_numeric(census['Inhabitants'].str.replace('.', ''))
    # Combine the census population data with the ShapeFile of seccionesCensales
    seccionesCensales_shp = loadShapeFile('data/secciones_censales/SECC_CE_20200101_MADRID.shp')
    census = census['Inhabitants']
    census = seccionesCensales_shp.join(census, on='CUSEC')
    return census


# function to obtain shapefile with distritos and their respective population count from the censal area shapefile
def get_distritos(census):

    distritos = loadShapeFile('data/distritos/DISTRITOS_20200101_MADRID.shp')
    dist_names = ['Centro','Arganzuela','Retiro','Salamanca','Chamartín','Tetuán','Chamberi','Fuencarral-El Pardo',
                  'Moncloa-Aravaca','Latina','Carabanchel','Usera','Puente de Vallecas','Moratalaz','Ciudad Lineal',
                  'Hortaleza','Villaverde','Villa de Vallecas','Vicálvaro','San-Blas Canillejas','Barajas']
    dist_inhabitants = [0] * 21
    # Use the inhabitants from the census areas and their CDIS value to get inhabitants in districts
    for i in range(len(census.index)):
        dist_inhabitants[int(census['CDIS'][i])-1] += census['Inhabitants'][i]
    distritos['Name'] = dist_names
    distritos['Inhabitants'] = dist_inhabitants

    return distritos


# function to obtain shapefile with barrios and their respective population count
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


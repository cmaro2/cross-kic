import os

from multiprocessing import Pool
from functools import partial

import gdal
import osr

import geopandas as gpd
import pandas as pd

from laspy.file import File
from shapely.geometry import Point

from PIL import Image
import numpy as np


def saveAsPNG(np_array, n):
    im = Image.fromarray(np_array.astype('uint8'))
    if n == [2]:
        string = 'ground'
    if n == [3, 4, 5]:
        string = 'vegetation'
    if n == [6]:
        string = 'building'
    im.save('output_' + string + '_5.png')

def saveAsGTIFF(np_array, n, xmin, xmax, ymin, ymax):

    if n == [2]:
        string = 'ground'
    if n == [3, 4, 5]:
        string = 'vegetation'
    if n == [6]:
        string = 'building'

    nx = np_array.shape[0]
    ny = np_array.shape[1]
    xres = (xmax-xmin)/nx
    yres = (ymax-ymin)/ny
    geotransform = [xmin, xres, 0, ymax, 0, -yres]


    dst_ds = gdal.GetDriverByName('GTiff').Create('output_' + string + '_5.tiff', ny, nx, 1, gdal.GDT_Byte)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(25830)
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(np_array)
    dst_ds.FlushCache()
    dst_ds = None


# Conversion function
if __name__ == '__main__':
    # Prepare
    input_file = 'data/LAS_4.las'
    f = File(input_file, mode='r')


    df = pd.DataFrame.from_records({
        'x': f.x,
        'y': f.y,
        'new_class': f.Classification,
        'blue': f.Blue,
        'green': f.Green,
        'red': f.Red
    })

    df_color = df

    df_color_x_min = df_color['x'].min()
    df_color_x_max = df_color['x'].max()
    df_color_y_min = df_color['y'].min()
    df_color_y_max = df_color['y'].max()

    m = 5

    bins_x = np.arange(df_color_x_min, df_color_x_max, m)
    ind_x = np.digitize(df_color['x'], bins_x)

    bins_y = np.arange(df_color_y_min, df_color_y_max, m)
    ind_y = np.digitize(df_color['y'], bins_y)

    def sort(index):
        return str(bins_x[ind_x[index]-1]) + ',' + str(bins_y[ind_y[index]-1])

    def aggregate(series):
        return series.value_counts().index[0]

    df_new = df_color.groupby(sort)
    df_grouped = df_new.agg(new_class=pd.NamedAgg(column='new_class', aggfunc=aggregate)).reset_index()

    new = df_grouped["index"].str.split(",", n=1, expand=True)
    df_grouped["x"] = new[0]
    df_grouped["y"] = new[1]

    n_array = [[2], [3,4,5], [6]]
    for n in n_array:
        final_df = df_grouped.loc[df_grouped['new_class'].isin(n)]
        final_df = final_df[['new_class', 'x', 'y']]

        np_array = np.array(final_df.pivot_table(index='x', columns='y', fill_value=0).replace([2,3,4,5,6], 255))

        np_array = np.rot90(np_array)

        saveAsPNG(np_array, n)
        saveAsGTIFF(np_array, n, df_color_x_min, df_color_x_max, df_color_y_min, df_color_y_max)

    #gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.x, df.y)])



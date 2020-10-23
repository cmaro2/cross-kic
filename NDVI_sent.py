import glob
import numpy as np
from osgeo import gdal
import rasterio

from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Open each band using gdal
band4 = rasterio.open('data/sentinel/sent_B04.jp2')
band8 = rasterio.open('data/sentinel/sent_B08.jp2')

# read in each band as array and convert to float for calculations
#raster sytem of reference
print(band4.crs)

#multiple band representation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
plot.show(band4, ax=ax1, cmap='Blues') #red
plot.show(band8, ax=ax2, cmap='Blues') #nir
fig.tight_layout()

#generate nir and red objects as arrays in float64 format
red = band4.read(1).astype('float64')
nir = band8.read(1).astype('float64')

#ndvi calculation, empty cells or nodata cells are reported as 0
ndvi=np.where(
    (nir+red)==0.,
    0,
    (nir-red)/(nir+red))


#export ndvi image
ndviImage = rasterio.open('out/ndviImage.tiff','w',
                          driver='Gtiff',
                          width=band4.width,
                          height = band4.height,
                          count=1, crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')

ndviImage.write(ndvi,1)
ndviImage.close()

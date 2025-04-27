#Imports
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from shapely.geometry import Point
import rasterio
from rasterio.transform import Affine
from rasterio.crs import CRS

#Read CSV
AQ_data_nit = pd.read_csv('AQ_data_nit.csv')

#Create points and values
points = list(zip(AQ_data_nit.X, AQ_data_nit.Y))
values = AQ_data_nit.Grid_data_.values

#Uncomment below to see list of points and/or values
#print(points)
#print(values)

#Set raster resolution
rRes = 50

#Create coordinates
xRange = np.arange(AQ_data_nit.X.min(),AQ_data_nit.X.max()+rRes,rRes)
yRange = np.arange(AQ_data_nit.Y.min(),AQ_data_nit.Y.max()+rRes,rRes)

#Create XY arrays
gridX,gridY = np.meshgrid(xRange, yRange)

#Interpolate using griddata
gridAQ = griddata(points, values, (gridX,gridY), method='linear')

#transform = Affine.translation(gridX[0][0]-rRes/2, gridY[0][0]-rRes/2)*Affine.scale(rRes,rRes)
#(transform)

#print(transform.__invert__() * transform)

#rasterCrs = CRS.from_epsg(27700)
#rasterCrs.data

#interpRaster = rasterio.open('Interp_Raster.tif',
                               # 'w',
                               # driver='GTiff',
                               # height=gridAQ.shape[0],
                               # width=gridAQ.shape[1],
                               # count=1,
                               # dtype=gridAQ.dtype,
                               # crs=rasterCrs,
                               # transform=transform,
                               # )
#interpRaster.write(gridAQ,1)
#interpRaster.close()



def export_raster(Z, XX, YY, min_x, max_x, min_y, max_y, proj, filename):
    '''Export and save a kernel density raster.'''

    # Get resolution
    xres = (max_x - min_x) / len(XX)
    yres = (max_y - min_y) / len(YY)

    # Set transform
    transform = Affine.translation(min_x - xres / 2, min_y - yres / 2) * Affine.scale(xres, yres)

    # Export array as raster
    with rasterio.open(
            filename,
            mode = "w",
            driver = "GTiff",
            height = gridAQ.shape[0],
            width = gridAQ.shape[1],
            count = 1,
            dtype = gridAQ.dtype,
            crs = proj,
            transform = transform,
    ) as new_dataset:
            new_dataset.write(gridAQ, 1)

# Export raster
export_raster(Z = Z_pk_krig, XX = XX_pk_krig, YY = YY_pk_krig,
                  min_x = min_x_rain, max_x = max_x_rain, min_y = min_y_rain, max_y = max_y_rain,
                  proj = proj, filename = "SAC_export.tif")
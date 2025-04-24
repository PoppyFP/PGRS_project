#Imports
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
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
rRes = 100

#Create coordinates
xRange = np.arange(AQ_data_nit.X.min(),AQ_data_nit.X.max()+rRes,rRes)
yRange = np.arange(AQ_data_nit.Y.min(),AQ_data_nit.Y.max()+rRes,rRes)

#Create XY arrays
gridX,gridY = np.meshgrid(xRange, yRange)

#Interpolate using griddata
gridAQ = griddata(points, values, (gridX,gridY), method='linear')

transform = Affine.translation(gridX[0][0]-rRes/2, gridY[0][0]-rRes/2)*Affine.scale(rRes,rRes)
transform

rasterCrs = CRS.from_epsg(27700)
rasterCrs.data

interpRaster = rasterio.open('Interp_Raster.tif',
                                'w',
                                driver='GTiff',
                                height=gridAQ.shape[0],
                                width=gridAQ.shape[1],
                                count=1,
                                dtype=gridAQ.dtype,
                                crs=rasterCrs,
                                transform=transform,
                                )
interpRaster.write(gridAQ,1)
interpRaster.close()
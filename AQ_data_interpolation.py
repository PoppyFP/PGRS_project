#imports
from cProfile import label

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pykrige.ok import OrdinaryKriging
import cartopy.crs as ccrs
import rasterio
import rasterio.mask
from rasterio.plot import show
from shapely.geometry import box

#Add CSV of Air Quality data
AQ_points = gpd.read_file('AQ_points.shp')

#Uncomment below to check CRS is EPSG:27700
#AQ_points.crs
#print(AQ_points.crs)

coords_AQ = [list(xy) for xy in zip(AQ_points["geometry"].x, AQ_points["geometry"].y)]
#print(coords_AQ)

x_AQ = AQ_points["geometry"].x
y_AQ = AQ_points["geometry"].y

#value_AQ = list(AQ_points["Grid_data_nit_dep"])

AQ_value = AQ_points.iloc[:, 3].tolist()
#print(AQ_points.iloc[:, 3].tolist())

min_x_AQ, min_y_AQ, max_x_AQ, max_y_AQ = AQ_points.total_bounds

#Run Ordinary Kriging using the PyKrige module
OK = OrdinaryKriging(
    np.array(x_AQ),
    np.array(y_AQ),
    AQ_value,
    variogram_model = "gaussian",
    verbose = False,
    enable_plotting = False,
    coordinates_type = "euclidean",
)

uk_utm = ccrs.UTM(30)

#Create figure for graph of interpolated points
fig = plt.figure(figsize = (10, 10))
ax = plt.axes(projection=uk_utm)

#Plot data
AQ_points.plot(ax = ax, marker = 'o', color = 'royalblue', markersize = 3, label = 'AQ_value')

for ind, row in AQ_points.iterrows():
    x, y = row.geometry.x, row.geometry.y
    ax.text(x, y, row['AQ_value'].title(), fontsize=7, transform=ccrs.PlateCarree())

#Save figure
fig.savefig('Interpolation.png', bbox_inches='tight', dpi=300)
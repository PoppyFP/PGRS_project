#Imports
import pandas as pd
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature

SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
AQ_points = gpd.read_file("AQ_points.shp")

SAC_AQ = gpd.clip(AQ_points, SAC_data)

#print(SAC_AQ)

#SAC_AQ.to_file('SAC_AQ')

SAC_AQ_points = gpd.read_file('SAC_AQ/SAC_AQ.shp')
SAC_AQ_points.crs
print(SAC_AQ_points.crs)

uk_utm = ccrs.UTM(30)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g', zorder=1)
ax.add_feature(SAC_feature)

SAC_AQ_plot = ax.plot(SAC_AQ_points.X, SAC_AQ_points.Y, 's', color='r', ms=2, markerfacecolor='r', transform=ccrs.UTM(30), zorder=2)

#SAC_AQ.plot(ax = ax, marker = 'o', color = 'royalblue', markersize = 3)

xmin, ymin, xmax, ymax = SAC_data.total_bounds # using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-3000, xmax+3000, ymin-3000, ymax+3000], crs=uk_utm)

fig.savefig('SAC_AQ.png', bbox_inches='tight', dpi=300)




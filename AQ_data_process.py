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

def AQ_clip (A, B, output_path):

    """Clip air quality point data by protected area polygon data
    Args:
        A = point data to be clipped
        B = polygon data e.g. from natural england, Special Areas of Conservation
        
    Returns: a GeoDataFrame of points within A which are within the selected polygon (B)"""

    aq_clipped = gpd.clip(A, B)
    aq_clipped.to_file(output_path)
    return AQ_clip

AQ_clip(AQ_points, SAC_data, 'SAC_AQ.shp')

SAC_AQ_points = gpd.read_file('SAC_AQ.shp')
SAC_AQ_points.crs

uk_utm = ccrs.UTM(30)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g', zorder=1)
ax.add_feature(SAC_feature)

SAC_AQ_plot = ax.plot(SAC_AQ_points.X, SAC_AQ_points.Y, 's', color='r', ms=2, markerfacecolor='r', transform=ccrs.UTM(30), zorder=2)

xmin, ymin, xmax, ymax = SAC_AQ_points.total_bounds
ax.set_extent([xmin-2000, xmax+2000, ymin-2000, ymax+2000], crs=uk_utm)

fig.savefig('SAC_AQ.png', bbox_inches='tight', dpi=300)




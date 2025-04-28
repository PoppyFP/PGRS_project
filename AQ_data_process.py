#Imports
import pandas as pd
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature

#Load data

Data_outline = gpd.read_file('Data_outline.shp')
SAC_data_full = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
SPA_data_full = gpd.read_file('NE_data/Special_Protection_Areas.gpkg')
SSSI_data_full = gpd.read_file('NE_data/Sites_Special_Scientific_Interest.gpkg')
AQ_points = gpd.read_file("AQ_points.shp")

Select_AQ_points = AQ_points[AQ_points['Grid_data_Nit_dep'] > 0.1]
print(Select_AQ_points)

#Clip Natural England data to the site

SAC_data = gpd.clip(SAC_data_full, Data_outline)
#SPA_data = gpd.clip(SPA_data_full, Data_outline)
#SSSI_data = gpd.clip(SSSI_data_full, Data_outline)

#Save clipped data to shapefiles

SAC_data.to_file('SAC_data.shp')
#SPA_data.to_file('SPA_data.shp')
#SSSI_data.to_file('SSSI_data.shp')

#Read saved shapefiles

SAC_data = gpd.read_file('SAC_data.shp')
#SPA_data = gpd.read_file('SPA_data.shp')
#SSSI_data = gpd.read_file('SSSI_data.shp')

#Define function to clip air quality data by polygon

def AQ_clip (A, B, output_path):

    """Clip air quality point data by protected area polygon data

    Parameters:

        A = point data to be clipped
        B = polygon data e.g. from natural england, Special Areas of Conservation
        
    Returns: a GeoDataFrame of points within A which are within the selected polygon (B)"""

    aq_clipped = gpd.clip(A, B)
    aq_clipped.to_file(output_path)

    return AQ_clip

#Run AQ_clip using AQ_points and one of the Natural England datasets

AQ_clip(AQ_points, SAC_data, 'AQ_clipped.shp')

#Read saved shapefile

AQ_clip_points = gpd.read_file('AQ_clipped.shp')

uk_utm = ccrs.UTM(30)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

Outline_feature = ShapelyFeature(Data_outline['geometry'], uk_utm, edgecolor='k', facecolor='w', zorder=0)
ax.add_feature(Outline_feature)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g', alpha = 0.5, zorder=1)
ax.add_feature(SAC_feature)

AQ_plot = ax.plot(AQ_clip_points.X, AQ_clip_points.Y, 'o', color='b', ms=2, markerfacecolor='b', transform=ccrs.UTM(30), zorder=2)

xmin, ymin, xmax, ymax = AQ_clip_points.total_bounds
ax.set_extent([xmin-1200, xmax+1200, ymin-1200, ymax+1200], crs=uk_utm)

gridlines = ax.gridlines(draw_labels=True,
                        # xlocs=[5, 10, 15, 20, 25, 30],
                        # ylocs=[54, 54.5, 55, 55.5])

#ax.add_artist(ScaleBar(distance_meters))

# def scale_bar(ax, length=5, location=(0.92, 0.95)):
#     """
#     Create a scale bar in a cartopy GeoAxes.
#
#     Parameters:
#
#     ax : cartopy.mpl.geoaxes.GeoAxes
#         the cartopy GeoAxes to add the scalebar to.
#
#     length : int, float (default 20)
#         the length of the scalebar, in km
#
#     location : tuple(float, float) (default (0.92, 0.95))
#         the location of the center right corner of the scalebar, in fractions of the axis.
#
#     Returns:
#
#     ax : cartopy.mpl.geoaxes.GeoAxes
#         the cartopy GeoAxes object
#
#     """
#     x0, x1, y0, y1 = ax.get_extent() # get the current extent of the axis
#     sbx = x0 + (x1 - x0) * location[0] # get the right x coordinate of the scale bar
#     sby = y0 + (y1 - y0) * location[1] # get the right y coordinate of the scale bar
#
#     ax.plot([sbx, sbx-length*500], [sby, sby], color='k', linewidth=4, transform=ax.projection) # plot a thick black line
#     ax.plot([sbx-(length/2)*500, sbx-length*500], [sby, sby], color='w', linewidth=2, transform=ax.projection) # plot a white line from 0 to halfway
#
#     ax.text(sbx, sby-(length/4)*100, f"{length} km", ha='center', transform=ax.projection, fontsize=6) # add a label at the right side
#     ax.text(sbx-(length/2)*500, sby-(length/4)*100, f"{int(length/2)} km", ha='center', transform=ax.projection, fontsize=6) # add a label in the center
#     ax.text(sbx-length*500, sby-(length/4)*100, '0 km', ha='center', transform=ax.projection, fontsize=6) # add a label at the left side
#
#     return ax
#
# scale_bar(ax)

#fig.savefig('clipped_AQ.png', bbox_inches='tight', dpi=300)
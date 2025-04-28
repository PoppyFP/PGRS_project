#Imports
import pandas as pd
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature

Data_outline = gpd.read_file('Data_outline.shp')
SAC_data_full = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
AQ_points = gpd.read_file("AQ_points.shp")

SAC_data = gpd.clip(SAC_data_full, Data_outline)

SAC_data.to_file('SAC_data.shp')

SAC_data = gpd.read_file('SAC_data.shp')

def AQ_clip (A, B, output_path):

    """Clip air quality point data by protected area polygon data

    Parameters:

        A = point data to be clipped
        B = polygon data e.g. from natural england, Special Areas of Conservation
        
    Returns: a GeoDataFrame of points within A which are within the selected polygon (B)"""

    aq_clipped = gpd.clip(A, B)
    aq_clipped.to_file(output_path)
    return AQ_clip

AQ_clip(AQ_points, SAC_data, 'SAC_AQ.shp')

SAC_AQ_points = gpd.read_file('SAC_AQ.shp')

uk_utm = ccrs.UTM(30)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

Outline_feature = ShapelyFeature(Data_outline['geometry'], uk_utm, edgecolor='k', facecolor='w', zorder=0)
ax.add_feature(Outline_feature)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g', alpha = 0.5, zorder=1)
ax.add_feature(SAC_feature)

SAC_AQ_plot = ax.plot(SAC_AQ_points.X, SAC_AQ_points.Y, 'o', color='b', ms=2, markerfacecolor='b', transform=ccrs.UTM(30), zorder=2)

xmin, ymin, xmax, ymax = SAC_AQ_points.total_bounds
ax.set_extent([xmin-1200, xmax+1200, ymin-1200, ymax+1200], crs=uk_utm)

#gridlines = ax.gridlines(draw_labels=True,
                        # xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                        # ylocs=[54, 54.5, 55, 55.5])
#gridlines.left_labels = False
#gridlines.bottom_labels = False


def scale_bar(ax, length=10, location=(0.92, 0.95)):
    """
    Create a scale bar in a cartopy GeoAxes.

    Parameters:

    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes to add the scalebar to.

    length : int, float (default 20)
        the length of the scalebar, in km

    location : tuple(float, float) (default (0.92, 0.95))
        the location of the center right corner of the scalebar, in fractions of the axis.

    Returns:

    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes object

    """
    x0, x1, y0, y1 = ax.get_extent() # get the current extent of the axis
    sbx = x0 + (x1 - x0) * location[0] # get the right x coordinate of the scale bar
    sby = y0 + (y1 - y0) * location[1] # get the right y coordinate of the scale bar

    ax.plot([sbx, sbx-length*500], [sby, sby], color='k', linewidth=4, transform=ax.projection) # plot a thick black line
    ax.plot([sbx-(length/2)*500, sbx-length*500], [sby, sby], color='w', linewidth=2, transform=ax.projection) # plot a white line from 0 to halfway

    ax.text(sbx, sby-(length/4)*100, f"{length} km", ha='center', transform=ax.projection, fontsize=6) # add a label at the right side
    ax.text(sbx-(length/2)*500, sby-(length/4)*100, f"{int(length/2)} km", ha='center', transform=ax.projection, fontsize=6) # add a label in the center
    ax.text(sbx-length*500, sby-(length/4)*100, '0 km', ha='center', transform=ax.projection, fontsize=6) # add a label at the left side

    return ax

scale_bar(ax)

fig.savefig('SAC_AQ.png', bbox_inches='tight', dpi=300)




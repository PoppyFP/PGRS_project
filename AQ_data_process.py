#Imports
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#Load data

Data_outline = gpd.read_file('Input_data/Data_outline.shp')
SAC_data_full = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
SPA_data_full = gpd.read_file('NE_data/Special_Protection_Areas.gpkg')
SSSI_data_full = gpd.read_file('NE_data/Sites_Special_Scientific_Interest.gpkg')
AQ_points = gpd.read_file('Input_data/AQ_points.shp')

#Select points above 0.1 (example using nitrogen data)

Select_AQ_points = AQ_points[AQ_points['Nit_data'] > 0.1]
Select_AQ_points.to_file('AQ_points_nit_0.1.shp')
Nit_data = gpd.read_file('AQ_points_nit_0.1.shp')

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

def AQ_clip (A, B, output_path, output_path_2):

    """Clip air quality point data by protected area polygon data

    Parameters:

        A = point data to be clipped
        B = polygon data e.g. from natural england, Special Areas of Conservation
        1st output path = shapefile name
        2nd output path = csv name
        
    Returns: a GeoDataFrame of points within A which are within the selected polygon (B)"""

    aq_clipped = gpd.clip(A, B)
    aq_clipped.to_file(output_path)
    aq_clipped.drop('geometry', axis=1).to_csv(output_path_2)

    return AQ_clip

#Run AQ_clip using AQ_points and one of the Natural England datasets

AQ_clip(Nit_data, SAC_data, 'AQ_clipped.shp', 'SAC_Nit_Data.csv')

#Read saved shapefile

AQ_clip_points = gpd.read_file('AQ_clipped.shp')

uk_utm = ccrs.UTM(30)

#Create figure and axes

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

#Add data to figure

Outline_feature = ShapelyFeature(Data_outline['geometry'], uk_utm, edgecolor='k', facecolor='w', zorder=0)
ax.add_feature(Outline_feature)

NE_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g', alpha = 0.5, zorder=1)
ax.add_feature(NE_feature)

AQ_plot = ax.plot(AQ_clip_points.X, AQ_clip_points.Y, 'o', color='b', ms=2, markerfacecolor='b', transform=ccrs.UTM(30), zorder=2)

#Set figure bounds/extents

xmin, ymin, xmax, ymax = AQ_clip_points.total_bounds
ax.set_extent([xmin-1200, xmax+1200, ymin-1200, ymax+1200], crs=uk_utm)

#Add north arrow (adapted from https://stackoverflow.com/questions/58088841/how-to-add-a-north-arrow-on-a-geopandas-map)

x, y, arrow_length = 0.05, 0.97, 0.1
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20,
            xycoords=ax.transAxes)

#Add scale bar (adapted from EGM722 Week 2: mapping with cartopy)

def scale_bar(ax, length=5, location=(0.92, 0.95)):
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

    ax.text(sbx, sby-(length/4)*200, f"{length} km", ha='center', transform=ax.projection, fontsize=6) # add a label at the right side
    ax.text(sbx-(length/2)*500, sby-(length/4)*200, f"{int(length/2)} km", ha='center', transform=ax.projection, fontsize=6) # add a label in the center
    ax.text(sbx-length*500, sby-(length/4)*200, '0 km', ha='center', transform=ax.projection, fontsize=6) # add a label at the left side

    return ax

scale_bar(ax)

#Add clipped OpenStreetMap basemap (adapted from https://stackoverflow.com/questions/65387500/insert-a-png-image-in-a-matplotlib-figure)

arr_img = plt.imread('Input_data/Site_Map.png')
im = OffsetImage(arr_img, zoom = 0.61)
ab = AnnotationBbox(im, (0.915, 0.04), xycoords='axes fraction',box_alignment=(1.0,-0.1), zorder=0, alpha=0.6)
ax.add_artist(ab)

#Export figure

fig.savefig('clipped_AQ.png', bbox_inches='tight', dpi=300)
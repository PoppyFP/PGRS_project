#imports
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

#Add protected areas polygon datasets
SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
#SPA_data = gpd.read_file('NE_data/Special_Protection_Areas.gpkg')
#SSSI_data = gpd.read_file('NE_data/Sites_Special_Scientific_Interest.gpkg')
AQ_points = gpd.read_file("AQ_points.shp")

#Check CRSs

#SAC_data.crs
#SPA_data.crs
#SSSI_data.crs
#AQ_points.crs

#print(SAC_data.crs)
#print(SPA_data.crs)
#print(SSSI_data.crs)
#print(AQ_points.crs)

AQ_points_crs = AQ_points.to_crs(epsg=27700)

clipped = []
for row, ind in SAC_data['OBJECTID'].unique(): # iterate over unique values of county
    tmp_clip = gpd.clip(AQ_points, SAC_data[SAC_data['OBJECTID']])
    #tmp_clip['Length'] = tmp_clip['geometry'].length / 1000 # remember to update the length for any clipped roads
    #tmp_clip['CountyName'] = county # set the county name for each road feature

    clipped.append(tmp_clip) # add the clipped GeoDataFrame to the list

print(clipped)

#join = gpd.sjoin(AQ_points, SAC_data, how='inner', lsuffix='left', rsuffix='right')
#print(join)

j#oin.to_csv('joinSAC.csv', index=False)

#Add CSV of Air Quality data
#df = pd.read_csv('joinSAC.csv')

#Uncomment below to show the CSV data
#print(df)

#Create geometry from the XY data in the AQ CSV
#df['geometry'] = list(zip(df['X'], df['Y']))
#df['geometry'] = df['geometry'].apply(Point)

#Create GeoDataFrames from the DataFrames
#gdf_AQ_SAC = gpd.GeoDataFrame(df)
#print(gdf_AQ_SAC)

#gdf_AQ_SAC.to_file(gdf_AQ_SAC.shp)

uk_utm = ccrs.UTM(30)
ccrs.CRS(SAC_data.crs)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g')
ax.add_feature(SAC_feature)

AQ_points.plot(ax = ax, marker = 'o', color = 'royalblue', markersize = 3)

xmin, ymin, xmax, ymax = SAC_data.total_bounds # using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-3000, xmax+3000, ymin-3000, ymax+3000], crs=uk_utm)

fig.savefig('SAC_join.png', bbox_inches='tight', dpi=300)
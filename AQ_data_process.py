#imports
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

#Add protected areas polygon datasets
SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
SPA_data = gpd.read_file('NE_data/Special_Protection_Areas.gpkg')
SSSI_data = gpd.read_file('NE_data/Sites_Special_Scientific_Interest.gpkg')

gdf_SAC = gpd.GeoDataFrame(SAC_data)

#Add CSV of Air Quality data
df = pd.read_csv('AQ_data.csv')

#Uncomment below to show the CSV data
#print(df)

#Create geometry from the XY data in the AQ CSV
df['geometry'] = list(zip(df['X'], df['Y']))
df['geometry'] = df['geometry'].apply(Point)

#Uncomment below to show the CSV data, which should now have an added 'geometry' column with POINT (X, Y) in for each row
#print(df)

#Create a GeoDataFrame from the DataFrame
gdf_nit = gpd.GeoDataFrame(df)
gdf_acid = gpd.GeoDataFrame(df)

#Select data over 0.1% and create new GeoDataFrames with the selected values
selected_rows_nit = gdf_nit[gdf_nit['Grid_data_Nit_dep'] > 0.1]
gdf_nit_select = gpd.GeoDataFrame(selected_rows_nit)

selected_rows_acid = gdf_acid[gdf_acid['Grid_data_Acid_dep'] > 0.1]
gdf_acid_select = gpd.GeoDataFrame(selected_rows_acid)

#Delete the acid data from the nitrogen dataset and the nitrogen data from the acid dataset
del gdf_nit_select['Grid_data_Acid_dep']
del gdf_acid_select['Grid_data_Nit_dep']

#Set GeoDataFrame CRS to EPSG:27700 (OSGB36/British National Grid)
gdf_nit_select = gdf_nit_select.set_crs("EPSG:27700")
gdf_acid_select = gdf_acid_select.set_crs("EPSG:27700")

#Save GeoDataFrame to geopackage
gdf_nit_select.to_file('AQ_points_nit_0.1.gpkg')
gdf_acid_select.to_file('AQ_points_acid_0.1.gpkg')

#Nit_data = gpd.read_file('AQ_points_nit_0.1.gpkg')
#Acid_data = gpd.read_file('AQ_points_acid_0.1.gpkg')

#Create list of protected areas for use in loop?
#list = [SAC_data, SPA_data, SSSI_data]
#for item in list:
    #join_list = gpd.sjoin(gdf_nit_select, )

#Or join one at a time?
#join_SAC_nit = gpd.sjoin(SAC_data, gdf_nit_select, how='inner', lsuffix='left', rsuffix='right')
#SAC_nit = gpd.GeoDataFrame(join_SAC_nit)
#join_SPA_nit = gpd.sjoin(SPA_data, gdf_nit_select, how='inner', lsuffix='left', rsuffix='right')
#print(join_SPA_nit)
#join_SSSI_nit = gpd.sjoin(SSSI_data, gdf_nit_select, how='inner', lsuffix='left', rsuffix='right')
#print(join_SSSI_nit)
#join_SAC_acid = gpd.sjoin(SAC_data, gdf_acid_select, how='inner', lsuffix='left', rsuffix='right')
#print(join_SAC_acid)
#join_SPA_acid = gpd.sjoin(SPA_data, gdf_acid_select, how='inner', lsuffix='left', rsuffix='right')
#print(join_SPA_acid)
#join_SSSI_acid = gpd.sjoin(SSSI_data, gdf_acid_select, how='inner', lsuffix='left', rsuffix='right')
#print(join_SSSI_acid)

#Or clip nitrogen and acid deposition data to protected area polygons?
SAC_nit_clip = gdf_nit_select[gdf_nit_select.geometry.within(SAC_data)]
print(SAC_nit_clip)

#Create figures with the joined data
uk_utm = ccrs.UTM(30)
ccrs.CRS(SAC_data.crs)

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=uk_utm)

SAC_feature = ShapelyFeature(SAC_data['geometry'], uk_utm, edgecolor='g', facecolor='g')
ax.add_feature(SAC_feature)

xmin, ymin, xmax, ymax = SAC_data.total_bounds # using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-3000, xmax+3000, ymin-3000, ymax+3000], crs=uk_utm)

fig.savefig('SAC.png', bbox_inches='tight', dpi=300)
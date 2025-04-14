#imports
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

#Add protected areas polygon datasets
SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')
SPA_data = gpd.read_file('NE_data/Special_Protection_Areas.gpkg')
SSSI_data = gpd.read_file('NE_data/Sites_Special_Scientific_Interest.gpkg')

#Add CSV of Air Quality data
df = pd.read_csv('AQ_data.csv')

#Uncomment below to show the CSV data
#print(df)

#Create points from the XY data in the AQ CSV
df['geometry'] = list(zip(df['X'], df['Y']))
df['geometry'] = df['geometry'].apply(Point)

#Uncomment below to show the CSV data, which should now have an added 'geometry' column with POINT (X, Y) in for each row
#print(df)

#Uncomment below to delete the separate 'X' and 'Y' columns, as they are now extraneous
#del df['X'], df['Y']

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

#Next step: spatial join
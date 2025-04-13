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

#Uncomment below to delete the seperate 'X' and 'Y' columns, as they are now extraneous
#del df['X'], df['Y']

#Create a GeoDataFrame from the DataFrame
gdf = gpd.GeoDataFrame(df)

#Set GeoDataFrame CRS to EPSG:27700 (OSGB36/British National Grid)
gdf = gdf.set_crs("EPSG:27700")

#Save GeoDataFrame to geopackage
gdf.to_file('AQ_points.gpkg')

#Next step: spatial join
#Imports
import pandas as pd

#Read CSV
AQ_data_nit = pd.read_csv('AQ_data_nit.csv')

#Create points and values
points = list(zip(AQ_data_nit.X, AQ_data_nit.Y))
values = AQ_data_nit.Grid_data_.values

SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')

clipped = []
for ind, row in points['values'].unique():
    tmp_clip = gpd.clip(SAC_data, points[points['values'] == points])
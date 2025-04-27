#Imports
import pandas as pd
import geopandas as gpd
import csv
import numpy as np

#Read CSV
#AQ_data_nit = pd.read_csv('AQ_data_nit.csv')

#Create points and values
#points = list(zip(AQ_data_nit.X, AQ_data_nit.Y))
#values = AQ_data_nit.Grid_data_.values

SAC_data = gpd.read_file('NE_data/Special_Area_of_Conservation.gpkg')

# Convert CSV data to list
with open('AQ_data_nit.csv', newline='') as f:
        reader = csv.reader(f)
        csv_data = list(reader)

input_data = np.asarray(csv_data)

clipped = []
for ind, row in csv_data[0].unique():
    tmp_clip = gpd.clip(SAC_data,csv_data[csv_data[0] == csv_data])
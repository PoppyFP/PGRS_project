#Imports
import csv
import numpy as np

#Convert CSV data to list
with open('AQ_data_nit.csv', newline='') as f:
    reader = csv.reader(f)
    csv_data = list(reader)

#Uncomment below to print list
#print(csv_data)

input_data = np.asarray(csv_data)

lon_lat_data = input_data[:, 0:2]
qff_values = input_data[:, 2]


#Imports
import csv
import numpy as np
import matplotlib.pyplot as plt

#Convert CSV data to list
with open('AQ_data_nit.csv', newline='') as f:
    reader = csv.reader(f)
    csv_data = list(reader)

#Uncomment below to print list
#print(csv_data)

#Convert list to array
input_data = np.asarray(csv_data)

lon_lat_data = input_data[:, 0:2]
qff_values = input_data[:, 2]

# definition of a 12° x 12° grid starting at 9°W / 47°N
resolution = 32.0
step = 1.0 / resolution
x0 = np.asarray([414891, 356154], dtype=np.float64)
size = (int(12.0 / step), int(12.0 / step))

#Calculate Barnes interpolation
from fastbarnes import interpolation
sigma = 1.0
field = interpolation.barnes(lon_lat_data, qff_values, sigma, x0, step, size)

#Create figure
plt.figure(figsize=(5, 5))
plt.margins(x=0, y=0)

gridX = np.arange(x0[0], x0[0]+size[1]*step, step)
gridY = np.arange(x0[1], x0[1]+size[0]*step, step)
levels = np.arange(976, 1026, 2)
cs = plt.contour(gridX, gridY, field, levels)
plt.clabel(cs, levels[::2], fmt='%d', fontsize=9)

plt.scatter(lon_lat_data[:, 0], lon_lat_data[:, 1], color='red', s=20, marker='.')

plt.show()
#imports
import pandas as pd
import geopandas as gpd
import numpy as np
from pykrige.ok import OrdinaryKriging
import rasterio
import rasterio.mask

#Add CSV of Air Quality data
AQ_points = gpd.read_file('AQ_points.shp')

#Uncomment below to check CRS is EPSG:27700
#AQ_points.crs
#print(AQ_points.crs)

coords_AQ = [list(xy) for xy in zip(AQ_points["geometry"].x, AQ_points["geometry"].y)]
#print(coords_AQ)

x_AQ = AQ_points["geometry"].x
y_AQ = AQ_points["geometry"].y

#value_AQ = list(AQ_points["Grid_data_nit_dep"])

AQ_value = AQ_points.iloc[:, 3].tolist()
#print(AQ_points.iloc[:, 3].tolist())

min_x_AQ, min_y_AQ, max_x_AQ, max_y_AQ = AQ_points.total_bounds

def export_raster(Z, XX, YY, min_x, max_x, min_y, max_y, proj, filename):
    '''Export and save a kernel density raster.'''

    # Get resolution
    xres = (max_x - min_x) / len(XX)
    yres = (max_y - min_y) / len(YY)

    # Set transform
    transform = Affine.translation(min_x - xres / 2, min_y - yres / 2) * Affine.scale(xres, yres)

    # Export array as raster
    with rasterio.open(
            filename,
            mode = "w",
            driver = "GTiff",
            height = gridAQ.shape[0],
            width = gridAQ.shape[1],
            count = 1,
            dtype = gridAQ.dtype,
            crs = proj,
            transform = transform,
    ) as new_dataset:
            new_dataset.write(gridAQ, 1)

XX_AQ_krig = np.linspace(min_x_AQ, max_x_AQ, 100)
YY_AQ_krig = np.linspace(min_y_AQ, max_y_AQ, 100)

#Run Ordinary Kriging using the PyKrige module
OK = OrdinaryKriging(
    np.array(x_AQ),
    np.array(y_AQ),
    AQ_value,
    variogram_model = "gaussian",
    verbose = False,
    enable_plotting = False,
    coordinates_type = "euclidean",

export_raster(Z = Z_pk_krig, XX = XX_pk_krig, YY = YY_pk_krig,
                  min_x = min_x_AQ, max_x = max_x_AQ, min_y = min_y_AQ, max_y = max_y_AQ,
                  proj = proj, filename = "export_raster.tif")



# uk_utm = ccrs.UTM(30)
#
# #Create figure for graph of interpolated points
# fig = plt.figure(figsize = (10, 10))
# ax = plt.axes(projection=uk_utm)
#
# #Plot data
# AQ_points.plot(ax = ax, marker = 'o', color = 'royalblue', markersize = 3, label = 'AQ_value')
#
# for ind, row in AQ_points.iterrows():
#     x, y = row.geometry.x, row.geometry.y
#     ax.text(x, y, row['AQ_value'].title(), fontsize=7, transform=ccrs.PlateCarree())
#
# #Save figure
# fig.savefig('Interpolation.png', bbox_inches='tight', dpi=300)
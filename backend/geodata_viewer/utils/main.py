from config import DB_CREDENTIALS, SUPPLIES_PATH
from data_utils import check_db_connection, csv_to_geodataframe
from raster_utils import load_raster
from plot_utils import plot_geodata
import sys
import os

# Añadir el directorio al sys.path
sys.path.append(os.path.abspath('/home/juanse/Climetrica/backend/data_wharehouse'))

if __name__ == "__main__":
    check_db_connection(DB_CREDENTIALS)
    # csv_path = f'{SUPPLIES_PATH}/sample_points2.csv'
    # points_gdf = csv_to_geodataframe(csv_path, lon_col='x', lat_col='y')
    # raster_path = './temperatura_mar_interpolado.tif'
    # raster_data, xs, ys, _, _ = load_raster(raster_path)
    # plot_geodata(points_gdf=points_gdf, raster_data=raster_data, xs=xs, ys=ys, title='Mapa combinado')

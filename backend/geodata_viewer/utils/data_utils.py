import pandas as pd
import geopandas as gpd

def check_db_connection(credentials):
    from db_utils import check_database_connection
    check_database_connection(credentials)

def csv_to_geodataframe(csv_path, lon_col, lat_col, crs=4326):
    df = pd.read_csv(csv_path)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]))
    gdf.set_crs(epsg=crs, inplace=True)
    return gdf

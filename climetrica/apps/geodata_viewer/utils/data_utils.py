# data_utils.py


from apps.data_conditioning.db_utils import check_database_connection, consult_data_by_fields
import geopandas as gpd
from shapely import wkt

def check_db_connection(credentials):
    return check_database_connection(credentials)

def load_geodata_from_db(credentials, variable, source, start_date, end_date):
    ok, *msg = check_database_connection(credentials)
    if not ok:
        raise ConnectionError(f"❌ No se pudo conectar a la base de datos: {msg}")

    where = f"""
        variable = '{variable}'
        AND fuente = '{source}'
        AND fecha BETWEEN '{start_date}' AND '{end_date}'
    """

    df = consult_data_by_fields(credentials, table_name='datos_geoespaciales', where=where)

    if 'geometry' in df.columns:
        df['geometry'] = df['geometry'].apply(wkt.loads)
        return gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')
    else:
        raise ValueError("❌ La tabla no tiene columna 'geometry'")

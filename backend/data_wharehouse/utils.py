import logging
import numpy as np
import re
from colorama import Fore, Style

from constants import *
from db_utils import *

def verbosity(msg: str, verb: bool = True, tl: int = 1,
               pref: str = '-', prompt: str = '> ',
               level: str = 'info'):
    '''
    Show logs and save them in log file
    v2.2.0
    '''

    if verb:
        pref *= tl
        if level == 'info':
            logging.info(f'{pref}{prompt}{msg}{Style.RESET_ALL}')
        elif level == 'error':
            logging.error(f'{Fore.RED}\033[1m{pref}{prompt}{msg}{Style.RESET_ALL}')
        elif level == 'success':
            logging.info(f'{Fore.GREEN}\033[1m{pref}{prompt}{msg}{Style.RESET_ALL}')
        elif level == 'notif':
            logging.info(f'{Fore.CYAN}\033[1m{pref}{prompt}{msg}{Style.RESET_ALL}')

def generate_alias(elms):
    drop_numbers = lambda s: re.sub(r'\d+', '', s)
    dic_alias = {}
    for elm in elms:
        al = ''.join([s[0] for s in elm.split('_')])
        if al in dic_alias.values():
            n = len([s for s in dic_alias.values() if drop_numbers(s) == al])
            dic_alias[elm] = f'{al}{n+1}'
        else:
            dic_alias[elm] = al
    return dic_alias

def haversine(lon1, lat1, lon2, lat2):
    '''Function for calculating the Haversine distance between two points'''
    # - Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # - Difference between longitudes and latitudes
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    # - Haversine Formula
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371
    # - Result in kilometers
    return c * r

def extract_data_from_data_warehouse(dic_credentials, request, tl_ini=1):
    '''Dedicated function for data consumption from the data warehouse.
    v1.0.0
    '''

    # - Connect to data wharehouse
    verbosity('Conectando con bodega de datos...', tl=tl_ini)
    try:
        conn = psycopg2.connect(**dic_credentials)
        verbosity('Conexion exitosa', tl=tl_ini+1, level='notif')
    except Exception as e:
        verbosity(f'Fallo al conectar con bodega de datos: {e}',
                    tl=tl_ini+1, level='error')
        raise e

    # - Conditioning parameters
    verbosity('Acondicionando parametros...', tl=tl_ini)
    data_type = request['data_type']
    if data_type not in ('temporal_serie', 'geodata'):
        s = 'Formato de dato solicitado no valido.'
        verbosity(s, tl=tl_ini+1, level='error')
        raise ValueError(s)
    id_source = dic_sources[request['source']]
    start_date, end_date = [request[k].replace('T', ' ') for k in ('start_date', 'end_date')]
    longitude, latitude = [request[k] for k in ('longitude', 'latitude')]
    ks = 'dim_name','fact_name','fact_table', 'fact_dim_name', 'iddim'

    dic_out = {}
    verbosity('Consultando datos por variable...', tl=tl_ini)
    for variable in request['variable']:
        verbosity(f'{variable}', tl=tl_ini+1, prompt='>> ')
        # - Get variable associated fields info
        dim_name, fact_name, fact_table, fact_dim_name, iddim = [dic_variables[variable][k] for k in ks]
        # - Generate alias for tables
        dic_alias = generate_alias([dim_name, fact_table])
        # - Consult data
        verbosity('Consultando datos...', tl=tl_ini+2)
        # -- Buil query
        # --- Fields
        fields = [
            'dd.date',
            'dc.longitude_latitude',
            f'{dic_alias[fact_table]}.{fact_name}',
        ]
        # --- Replace values
        query = f"select <fields> \
        from {fact_table} {dic_alias[fact_table]} \
        join {dim_name} {dic_alias[dim_name]} on \
        {dic_alias[dim_name]}.{iddim} = \
        {dic_alias[fact_table]}.{fact_dim_name} \
        join dim_coordinates dc on dc.iddim_coordinates = {dic_alias[fact_table]}.dim_coordinates_iddim_coordinates \
        join dim_date dd on dd.iddim_date = {dic_alias[fact_table]}.dim_date_iddim_date \
        where {dic_alias[dim_name]}.source = {id_source} \
        and dd.date >= '{start_date}' \
        and dd.date <= '{end_date}' \
        order by dd.date asc;"
        query = query.replace('<fields>', ', '.join(fields))
        df = consult_data(conn, query, use_cursor_columns=True)
        conn.close()
        if df.empty:
            verbosity('No se encontraron datos en la consulta', tl=tl_ini+3, level='error')
            dic_out[variable] = None
        else:
            df[fact_name] = df[fact_name].astype(float)
            if data_type == 'temporal_serie':
                verbosity('Extrayendo serie temporal...', tl=tl_ini+2)
                # - Find the nearest coordinate
                # -- Coordinates without repeating
                verbosity('Buscando coordenada mas cercana...', tl=tl_ini+2)
                df_lonlat = pd.DataFrame(df['longitude_latitude'].copy().drop_duplicates())
                df_lonlat[['longitude', 'latitude']] = df_lonlat['longitude_latitude'].str.split(',', expand=True)
                df_lonlat['longitude'] = df_lonlat['longitude'].astype(float)
                df_lonlat['latitude'] = df_lonlat['latitude'].astype(float)
                # -- Find nearest longitude_latitude with haversine
                nearest_row_index = df_lonlat.apply(
                    lambda row: haversine(longitude, latitude, row['longitude'], row['latitude']), axis=1).idxmin()
                nearest_longitude_latitude = df_lonlat.loc[nearest_row_index, 'longitude_latitude']
                verbosity(nearest_longitude_latitude, tl=tl_ini+3, level='notif')

                # - Filter values
                verbosity('Filtrando valores...', tl=tl_ini+2)
                df = df[df['longitude_latitude'] == nearest_longitude_latitude]
                df.drop(columns=['longitude_latitude'], inplace=True)
                df.reset_index(drop=True, inplace=True)
                df['date'] = df['date'].apply(lambda d: d.isoformat())
                verbosity(f'{len(df)} fechas extraidas.',
                            tl=tl_ini+3, level='notif')
                dic_out[variable] = df.to_dict(orient='list')
            else:
                verbosity('Extrayendo datos georreferenciados...', tl=tl_ini+2)
                # - Formatting coordinates
                df[['longitude', 'latitude']] = df['longitude_latitude'].str.split(',', expand=True)
                df['longitude'] = df['longitude'].astype(float)
                df['latitude'] = df['latitude'].astype(float)
                df.drop(columns=['longitude_latitude'], inplace=True)
                # - Group by dates
                verbosity('Agrupando por fechas...', tl=tl_ini+2)
                gr_dates = df.groupby('date')
                verbosity(f'{len(gr_dates)} conjuntos segmentados', tl=tl_ini+3)
                dic_out[variable] = {}
                for date in gr_dates.groups.keys():
                    sdf = gr_dates.get_group(date)
                    sdf = sdf[['longitude', 'latitude', fact_name]]
                    sdf = sdf.sort_values(['longitude', 'latitude'])
                    dic_out[variable][date.isoformat()] = sdf.to_dict(orient='list')
    verbosity('Rutina finalizada', tl=tl_ini, level='notif')
    return dic_out

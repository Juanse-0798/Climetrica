from typing_extensions import Dict, Sequence
import psycopg2
from psycopg2.extensions import connection
import pandas as pd
import numpy as np

def check_database_connection(dic_credentials: Dict):
    '''
    ...
    v1.0.0
    '''

    try:
        connection = psycopg2.connect(**dic_credentials)
        connection.close()
        print("✅ Conexión a la base de datos exitosa")
        return True,
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False,f'{type(e).__name__}, {str(e)}'
    

def consult_data_by_fields(connection_element: Dict|connection, table_name: str,
                           fields: Sequence = None, where: str = ''):
    '''
    ...
    v2.0.0
    '''

    # - Establish database connection
    connection = psycopg2.connect(**connection_element) if isinstance(connection_element, dict) else connection_element
    # - Where sentence
    sent_where = '' if where == '' else f' WHERE {where}'
    # - Do consult
    if fields is None:
        fields = consult_data(connection,
                              f"select column_name from information_schema.columns where table_name = '{table_name}'").flatten()
    data = consult_data(connection, f'SELECT {",".join(fields)} FROM {table_name}{sent_where};', columns=fields)

    # - Close connection if necessary
    if isinstance(connection_element, dict):
        connection.close()

    return data

def consult_data(connection_element: Dict|connection, query, varss=None, columns=None,
                 use_cursor_columns=False):
    '''
    v2.1.0
    '''

    connection = psycopg2.connect(**connection_element) if isinstance(connection_element, dict) else connection_element
    # - Instantiate cursor and execute query
    cursor = connection.cursor()
    cursor.execute(query,varss)
    column_names = [desc[0] for desc in cursor.description]
    # - Get data
    data = np.asarray(cursor.fetchall())
    cursor.close()
    if isinstance(connection_element, dict):
        connection.close()

    if columns is not None:
        if len(data) == 0:
            data = pd.DataFrame(columns=columns)
        else:
            data = pd.DataFrame(dict(zip(columns,data.T)))
    elif use_cursor_columns:
        if len(data) == 0:
            data = pd.DataFrame(columns=column_names)
        else:
            data = pd.DataFrame(data, columns=column_names)
    return data

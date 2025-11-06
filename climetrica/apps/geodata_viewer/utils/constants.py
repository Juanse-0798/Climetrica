from .config import DB_CREDENTIALS

DB_REQUESTS = {
    'nivel del mar': {
        'data_type': 'geodata',
        'variable': 'nivel del mar',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
        'longitude': None,
        'latitude': None
    },
    'temperatura del mar': {
        'data_type': 'geodata',
        'variable': 'temperatura del mar',
        'source': 'ERA5',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
        'longitude': None,
        'latitude': None
    },
    'direccion del viento': {
        'data_type': 'geodata',
        'variable': 'direccion del viento',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
        'longitude': None,
        'latitude': None
    },
    'velocidad del viento': {
        'data_type': 'geodata',
        'variable': 'velocidad del viento',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
        'longitude': None,
        'latitude': None
    },
    'precipitacion acumulada': {
        'data_type': 'geodata',
        'variable': 'precipitacion acumulada',
        'source': 'ERA5',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
        'longitude': None,
        'latitude': None
    }
}

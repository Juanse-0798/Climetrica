from .config import DB_CREDENTIALS

DB_REQUESTS = {
    'nivel del mar': {
        'variable': 'nivel del mar',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
    },
    'temperatura del mar': {
        'variable': 'temperatura del mar',
        'source': 'ERA5',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
    },
    'direccion del viento': {
        'variable': 'direccion del viento',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
    },
    'velocidad del viento': {
        'variable': 'velocidad del viento',
        'source': 'Copernicus',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
    },
    'precipitacion acumulada': {
        'variable': 'precipitacion acumulada',
        'source': 'ERA5',
        'start_date': '2015-06-30T00:00:00',
        'end_date': '2023-06-30T00:00:00',
    }
}

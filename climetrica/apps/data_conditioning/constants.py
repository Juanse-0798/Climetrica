
dic_variables = {
    'temperatura del aire': {
        'dim_name': 'dim_air_temperature',
        'fact_name': 'air_temperature',
        'fact_table': 'fact_meteorology',
        'fact_dim_name': 'dim_air_temperature_iddim_air_temperature',
        'iddim': 'iddim_air_temperature'
    },
    'presion atmosferica': {
        'dim_name': 'dim_atmospheric_pressure',
        'fact_name': 'atmospheric_pressure',
        'fact_table': 'fact_meteorology',
        'fact_dim_name': 'dim_atmospheric_pressure_iddim_atmospheric_pressure',
        'iddim': 'iddim_atmospheric_pressure'
    },
    'precipitacion acumulada': {
        'dim_name': 'dim_accumulated_precipitation',
        'fact_name': 'accumulated_precipitation',
        'fact_table': 'fact_meteorology',
        'fact_dim_name': 'dim_accumulated_precipitation_iddim_accumulated_precipitation',
        'iddim': 'iddim_accumulated_precipitation'
    },
    'presion barometrica': {
        'dim_name': 'dim_barometric_pressure',
        'fact_name': 'barometric_pressure',
        'fact_table': 'fact_meteorology',
        'fact_dim_name': 'dim_barometric_pressure_iddim_barometric_pressure',
        'iddim': 'iddim_barometric_pressure'
    },
    'humedad relativa': {
        'dim_name': 'dim_relative_humidity',
        'fact_name': 'relative_humidity',
        'fact_table': 'fact_meteorology',
        'fact_dim_name': 'dim_relative_humidity_iddim_relative_humidity',
        'iddim': 'iddim_relative_humidity'
    },
    'salinidad': {
        'dim_name': 'dim_salinity',
        'fact_name': 'salinity',
        'fact_table': 'fact_oceanography',
        'fact_dim_name': 'dim_salinity_iddim_salinity',
        'iddim': 'iddim_salinity'
    },
    'nivel del mar': {
        'dim_name': 'dim_sea_level',
        'fact_name': 'sea_level',
        'fact_table': 'fact_oceanography',
        'fact_dim_name': 'dim_sea_level_iddim_sea_level',
        'iddim': 'iddim_sea_level'
    },
    'temperatura del mar': {
        'dim_name': 'dim_sea_temperature',
        'fact_name': 'sea_temperature',
        'fact_table': 'fact_oceanography',
        'fact_dim_name': 'dim_sea_temperature_iddim_sea_temperature',
        'iddim': 'iddim_sea_temperature'
    },
    'direccion del viento': {
        'dim_name': 'dim_wind_direction',
        'fact_name': 'wind_direction',
        'fact_table': 'fact_oceanography',
        'fact_dim_name': 'dim_wind_direction_iddim_wind_direction',
        'iddim': 'iddim_wind_direction'
    },
    'velocidad del viento': {
        'dim_name': 'dim_wind_velocity',
        'fact_name': 'wind_velocity',
        'fact_table': 'fact_oceanography',
        'fact_dim_name': 'dim_wind_velocity_iddim_wind_velocity',
        'iddim': 'iddim_wind_velocity'
    }
}

dic_sources = {
    'Copernicus': 1,
    'ERA5': 2,
    'Giovanni NASA': 3
}

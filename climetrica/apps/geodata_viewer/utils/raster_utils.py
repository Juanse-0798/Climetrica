import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize

def load_raster(raster_file_path):
    with rasterio.open(raster_file_path) as src:
        data = src.read(1)
        transform = src.transform
        nodata = src.nodata
        data = np.where((data == nodata) | (data == 0), np.nan, data)
        height, width = data.shape
        cols, rows = np.meshgrid(np.arange(width), np.arange(height))
        xs, ys = rasterio.transform.xy(transform, rows, cols)
    return data, np.array(xs), np.array(ys), transform, nodata

def geodataframe_to_raster(gdf, value_column, resolution=0.03):
    minx, miny, maxx, maxy = gdf.total_bounds
    minx = np.floor(minx / resolution) * resolution
    maxx = np.ceil(maxx / resolution) * resolution
    miny = np.floor(miny / resolution) * resolution
    maxy = np.ceil(maxy / resolution) * resolution
    transform = from_origin(minx, maxy, resolution, resolution)
    shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[value_column]))
    raster = rasterize(
        shapes=shapes,
        out_shape=((int((maxy - miny) / resolution), int((maxx - minx) / resolution))),
        transform=transform,
        fill=0.0,
        dtype='float32'
    )
    return raster, transform, 0.0

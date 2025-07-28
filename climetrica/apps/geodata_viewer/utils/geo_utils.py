def convert_points_to_polygons(gdf, buffer_size=0.3):
    original_crs = gdf.crs
    gdf = gdf.to_crs(epsg=4326)
    gdf['geometry'] = gdf.geometry.buffer(buffer_size)
    gdf = gdf.to_crs(original_crs)
    return gdf

def extract_lines(gdf):
    import numpy as np
    lines = []
    for geom in gdf.geometry:
        if geom.geom_type == 'LineString':
            x, y = map(np.array, geom.xy)
            lines.append((x, y))
        elif geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                x, y = map(np.array, line.xy)
                lines.append((x, y))
    return lines

def extract_polygons(gdf):
    import numpy as np
    polygons = []
    for geom in gdf.geometry:
        if geom.geom_type == 'Polygon':
            x, y = geom.exterior.xy  
            x, y = map(np.array, (x, y))
            polygons.append((x, y))
            for interior in geom.interiors:
                x, y = interior.xy
                x, y = map(np.array, (x, y))
                polygons.append((x, y))
        elif geom.geom_type == 'MultiPolygon':
            for polygon in geom.geoms:
                x, y = polygon.exterior.xy  
                x, y = map(np.array, (x, y))
                polygons.append((x, y))
                for interior in polygon.interiors:
                    x, y = interior.xy
                    x, y = map(np.array, (x, y))
                    polygons.append((x, y))
    return polygons

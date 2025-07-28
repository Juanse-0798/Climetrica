import plotly.graph_objs as go

def plot_geodata(points_gdf=None, lines=None, polygons=None, raster_data=None, xs=None, ys=None, title='Mapa'):
    fig = go.Figure()
    if points_gdf is not None:
        fig.add_trace(go.Scatter(
            x=points_gdf.geometry.x,
            y=points_gdf.geometry.y,
            mode='markers',
            marker=dict(size=10, color='blue'),
            name="Points"
        ))
    if lines is not None:
        for x, y in lines:
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Lines'))
    if polygons is not None:
        for x, y in polygons:
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', fill='toself', name='Polygons'))
    if raster_data is not None and xs is not None and ys is not None:
        fig.add_trace(go.Heatmap(
            z=raster_data,
            x=xs[0],
            y=ys[:, 0],
            colorscale='YlOrRd',
            reversescale=True,
            name='Raster'
        ))
    fig.update_layout(
        title=title,
        xaxis_title='Longitud',
        yaxis_title='Latitud',
        width=900,
        height=600,
        template='plotly_white'
    )
    fig.show()

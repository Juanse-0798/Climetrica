import plotly.graph_objects as go
import numpy as np


def plot_heatmap_layers_map(layers_with_values):
    all_z = np.concatenate([z for _, _, z, _ in layers_with_values])
    zmin, zmax = np.min(all_z), np.max(all_z)

    fig = go.Figure()

    for name, gdf, z, colorscale in layers_with_values:
        fig.add_trace(go.Densitymapbox(
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            z=z,
            radius=50,
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            name=name,
            showscale=False,
            legendgroup=name,
            visible=True,
            hovertemplate="%{lat}, %{lon}<br>Valor: %{z}<br>Capa: " + name + "<extra></extra>"
            
        ))

        # ➤ Traza fantasma para la leyenda (activación/desactivación)
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(size=10, color="rgba(0,0,0,0)"),
            name=name,
            legendgroup=name,
            showlegend=True
        ))

    fig.update_layout(
        mapbox=dict(
            style='carto-positron',
            center=dict(
                lat=np.mean([gdf.geometry.y.mean() for _, gdf, _, _ in layers_with_values]),
                lon=np.mean([gdf.geometry.x.mean() for _, gdf, _, _ in layers_with_values])
            ),
            zoom=6
        ),
        margin=dict(r=0, t=30, l=0, b=0),
        height=700,
        showlegend=True
    )

    return fig


def plot_multiple_layers_map(layer_list):
    fig = go.Figure()

    for name, gdf in layer_list:
        fig.add_trace(go.Scattermapbox(
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            mode='markers',
            marker=dict(size=6),
            name=name,
            legendgroup=name,
            visible=True,
            hovertemplate="%{lat}, %{lon}<br>Capa: " + name + "<extra></extra>"
        ))

      

    fig.update_layout(
        mapbox=dict(
            style='carto-positron',
            center=dict(
                lat=np.mean([gdf.geometry.y.mean() for _, gdf in layer_list]),
                lon=np.mean([gdf.geometry.x.mean() for _, gdf in layer_list])
            ),
            zoom=6
        ),
        margin=dict(r=0, t=30, l=0, b=0),
        height=700,
        showlegend=True
    )

    return fig
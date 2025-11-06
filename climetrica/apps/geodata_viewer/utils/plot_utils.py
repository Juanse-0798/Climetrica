import plotly.graph_objects as go
import numpy as np


def plot_heatmap_layers_map(layers_with_values):
    # --- Verificación de datos ---
    if not layers_with_values or all(len(z) == 0 for _, _, z, _ in layers_with_values):
        print("🚫 No se encontraron datos válidos en layers_with_values.")
        # En vez de lanzar un error, devolvemos un mapa vacío con mensaje
        fig = go.Figure()
        fig.update_layout(
            annotations=[
                dict(
                    text="❌ No se encontraron datos válidos para mostrar en el mapa de calor.",
                    x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="red")
                )
            ],
            mapbox=dict(style='carto-positron', zoom=4, center=dict(lat=4.6, lon=-74.1))
        )
        return fig

    # --- Escala global ---
    all_z = np.concatenate([z for _, _, z, _ in layers_with_values if len(z) > 0])
    zmin, zmax = np.min(all_z), np.max(all_z)

    fig = go.Figure()

    for name, gdf, z, colorscale in layers_with_values:
        if gdf.empty:
            print(f"⚠️ Capa '{name}' está vacía. Se omite.")
            continue

        fig.add_trace(go.Densitymapbox(
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            z=z,
            radius=30,
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            name=name,
            showscale=False,
            legendgroup=name,
            hovertemplate=(
                "<b>%{lat:.4f}, %{lon:.4f}</b><br>"
                f"<b>Capa:</b> {name}<br>"
                "<b>Valor:</b> %{z}<extra></extra>"
            )
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
                lat=np.mean([gdf.geometry.y.mean() for _, gdf, _, _ in layers_with_values if not gdf.empty]),
                lon=np.mean([gdf.geometry.x.mean() for _, gdf, _, _ in layers_with_values if not gdf.empty])
            ),
            zoom=6
        ),
        margin=dict(r=0, t=30, l=0, b=0),
        height=700,
        showlegend=True
    )

    return fig


def plot_multiple_layers_map(layer_list):
    if not layer_list or all(gdf.empty for _, gdf in layer_list):
        print("🚫 No se encontraron datos válidos para mostrar en el mapa de puntos.")
        fig = go.Figure()
        fig.update_layout(
            annotations=[
                dict(
                    text="❌ No se encontraron datos válidos para mostrar en el mapa de puntos.",
                    x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="red")
                )
            ],
            mapbox=dict(style='carto-positron', zoom=4, center=dict(lat=4.6, lon=-74.1))
        )
        return fig

    fig = go.Figure()

    for name, gdf in layer_list:
        if gdf.empty:
            print(f"⚠️ Capa '{name}' vacía, omitida.")
            continue

        fig.add_trace(go.Scattermapbox(
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            mode='markers',
            marker=dict(size=6),
            name=name,
            legendgroup=name,
            hovertemplate=(
                "<b>%{lat:.4f}, %{lon:.4f}</b><br>"
                f"<b>Capa:</b> {name}<extra></extra>"
            )
        ))

        # ➤ Traza fantasma para la leyenda
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
                lat=np.mean([gdf.geometry.y.mean() for _, gdf in layer_list if not gdf.empty]),
                lon=np.mean([gdf.geometry.x.mean() for _, gdf in layer_list if not gdf.empty])
            ),
            zoom=6
        ),
        margin=dict(r=0, t=30, l=0, b=0),
        height=700,
        showlegend=True
    )

    return fig

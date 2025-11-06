import os
import numpy as np
import pandas as pd
import geopandas as gpd
from django.shortcuts import render

from .utils.plot_utils import plot_heatmap_layers_map, plot_multiple_layers_map
from apps.geodata_viewer.utils.config import DB_CREDENTIALS
from apps.geodata_viewer.utils.constants import DB_REQUESTS
from apps.data_conditioning.utils import extract_data_from_data_warehouse


def plot_map_view(request):
    plot_div = None
    layers = []  # [(nombre, gdf, z, colorscale)]

    if request.method == 'POST':
        render_type = request.POST.get('render_type', 'heatmap')
        print(f"📥 Tipo de render: {render_type}")

        # --- 1️⃣ Carga desde archivos CSV o GeoJSON ---
        uploaded_files = request.FILES.getlist('layer_files')
        if uploaded_files:
            print(f"📦 Archivos recibidos: {[f.name for f in uploaded_files]}")
            tmp_dir = os.path.join(os.getcwd(), "tmp")
            os.makedirs(tmp_dir, exist_ok=True)

            for uploaded_file in uploaded_files:
                temp_path = os.path.join(tmp_dir, uploaded_file.name)
                print(f"📂 Procesando archivo: {uploaded_file.name}")

                with open(temp_path, 'wb+') as dest:
                    for chunk in uploaded_file.chunks():
                        dest.write(chunk)

                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(temp_path)
                        if df.shape[1] < 3:
                            print(f"⚠️ {uploaded_file.name} no tiene suficientes columnas.")
                            continue

                        lon_col, lat_col, value_col = df.columns[:3]
                        df = df.dropna(subset=[lon_col, lat_col, value_col])
                        df = df[df[value_col] != 0]

                        gdf = gpd.GeoDataFrame(
                            df,
                            geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
                            crs="EPSG:4326"
                        )
                        z_values = df[value_col].values
                        colorscale = request.POST.get('colorscale', 'Turbo')
                        layers.append((uploaded_file.name, gdf, z_values, colorscale))

                    elif uploaded_file.name.endswith('.geojson'):
                        gdf = gpd.read_file(temp_path)
                        if 'value' in gdf.columns:
                            gdf = gdf.dropna(subset=['value'])
                            gdf = gdf[gdf['value'] != 0]
                            z_values = gdf['value'].values
                        else:
                            z_values = np.ones(len(gdf))

                        colorscale = request.POST.get('colorscale', 'Turbo')
                        layers.append((uploaded_file.name, gdf, z_values, colorscale))

                except Exception as e:
                    print(f"❌ Error procesando {uploaded_file.name}: {e}")

        # --- 2️⃣ Carga desde la bodega de datos ---
        db_variable = request.POST.get('db_variable')
        print(f"🧠 Variable de BD seleccionada: {db_variable}")
        if db_variable:
            try:
                req = DB_REQUESTS.get(db_variable)
                if not req:
                    print(f"⚠️ {db_variable} no encontrada en DB_REQUESTS.")
                else:
                    # Crear request compatible con extract_data_from_data_warehouse
                    request_dic = {
                        'data_type': 'geodata',
                        'variable': [req['variable']],
                        'source': req['source'],
                        'start_date': req['start_date'],
                        'end_date': req['end_date'],
                        'longitude': None,
                        'latitude': None
                    }

                    dic_out = extract_data_from_data_warehouse(DB_CREDENTIALS, request_dic)
                    data = dic_out.get(req['variable'])

                    if not data:
                        print(f"⚠️ No se recibieron datos válidos para {db_variable}")
                    else:
                        # 🔹 Combinar todas las fechas en un solo DataFrame
                        combined_df = pd.concat(
                            [pd.DataFrame(content) for content in data.values()],
                            ignore_index=True
                        )

                        combined_df = combined_df.dropna(subset=['longitude', 'latitude'])
                        var_name = req['variable']

                        if var_name in combined_df.columns:
                            combined_df = combined_df[combined_df[var_name] != 0]
                            z_values = combined_df[var_name].values
                        else:
                            z_values = np.ones(len(combined_df))

                        if combined_df.empty:
                            print(f"⚠️ Sin valores válidos para {db_variable}")
                        else:
                            gdf = gpd.GeoDataFrame(
                                combined_df,
                                geometry=gpd.points_from_xy(combined_df['longitude'], combined_df['latitude']),
                                crs="EPSG:4326"
                            )
                            colorscale = request.POST.get('colorscale', 'Turbo')
                            layers.append((db_variable, gdf, z_values, colorscale))

            except Exception as e:
                print(f"❌ Error cargando '{db_variable}' desde la bodega: {e}")

        # --- 3️⃣ Generar el mapa ---
        try:
            if not layers:
                raise ValueError("❌ No hay capas válidas para mostrar.")

            if render_type == 'heatmap':
                fig = plot_heatmap_layers_map(layers)
            else:
                fig = plot_multiple_layers_map([(name, gdf) for name, gdf, _, _ in layers])

            plot_div = fig.to_html(full_html=False)
        except ValueError as e:
            plot_div = f"<p style='color:red; font-weight:bold;'>{str(e)}</p>"
        except Exception as e:
            print(f"❌ Error inesperado al generar el mapa: {e}")
            plot_div = "<p style='color:red;'>Ocurrió un error al generar el mapa.</p>"

    return render(request, 'index.html', {'plot_div': plot_div})

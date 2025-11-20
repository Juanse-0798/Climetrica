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

        # recoger lista de colores seleccionados (uno por archivo subido, en el mismo orden)
        colors_list = request.POST.getlist('colors')  # <-- nuevo

        # --- 1️⃣ Carga desde archivos CSV o GeoJSON ---
        uploaded_files = request.FILES.getlist('layer_files')
        if uploaded_files:
            print(f"📦 Archivos recibidos: {[f.name for f in uploaded_files]}")
            tmp_dir = os.path.join(os.getcwd(), "tmp")
            os.makedirs(tmp_dir, exist_ok=True)

            for idx, uploaded_file in enumerate(uploaded_files):
                temp_path = os.path.join(tmp_dir, uploaded_file.name)
                print(f"📂 Procesando archivo: {uploaded_file.name}")

                with open(temp_path, 'wb+') as dest:
                    for chunk in uploaded_file.chunks():
                        dest.write(chunk)

                try:
                    # seleccionar colorscale específico para este archivo (si fue enviado)
                    colorscale = colors_list[idx] if idx < len(colors_list) and colors_list[idx] else request.POST.get('colorscale', 'Turbo')

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
                        layers.append((uploaded_file.name, gdf, z_values, colorscale))

                    elif uploaded_file.name.endswith('.geojson'):
                        gdf = gpd.read_file(temp_path)
                        if 'value' in gdf.columns:
                            gdf = gdf.dropna(subset=['value'])
                            gdf = gdf[gdf['value'] != 0]
                            z_values = gdf['value'].values
                        else:
                            z_values = np.ones(len(gdf))

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
                    # Asegurar que 'variable' en el request sea siempre una lista
                    raw_var = req.get('variable', db_variable)
                    if isinstance(raw_var, str):
                        variables = [raw_var]
                    elif isinstance(raw_var, (list, tuple)):
                        variables = list(raw_var)
                    else:
                        variables = [db_variable]

                    request_dic = {
                        'data_type': 'geodata',
                        'variable': variables,
                        'source': req.get('source'),
                        'start_date': req.get('start_date'),
                        'end_date': req.get('end_date'),
                        'longitude': None,
                        'latitude': None
                    }

                    dic_out = extract_data_from_data_warehouse(DB_CREDENTIALS, request_dic)

                    # Determinar la clave correcta en la respuesta
                    data_key = variables[0]
                    data = None
                    if isinstance(dic_out, dict):
                        if data_key in dic_out:
                            data = dic_out[data_key]
                        elif len(dic_out) == 1:
                            # tomar la única entrada si la clave no coincide exactamente
                            data_key, data = next(iter(dic_out.items()))
                        else:
                            # intentar buscar clave que contenga la palabra (por si vienen nombres distintos)
                            for k in dic_out.keys():
                                if db_variable in k or variables[0] in k:
                                    data = dic_out[k]
                                    data_key = k
                                    break

                    if not data:
                        print(f"⚠️ No se recibieron datos válidos para {db_variable}")
                    else:
                        # Combinar todas las fechas/entradas en un solo DataFrame
                        frames = []
                        if isinstance(data, dict):
                            for content in data.values():
                                frames.append(pd.DataFrame(content))
                        else:
                            frames.append(pd.DataFrame(data))

                        if not frames:
                            print(f"⚠️ No hay frames para {db_variable}")
                        else:
                            combined_df = pd.concat(frames, ignore_index=True)

                            # eliminar registros sin coordenadas
                            combined_df = combined_df.dropna(subset=['longitude', 'latitude'], how='any')
                            if combined_df.empty:
                                print(f"⚠️ Sin coordenadas válidas para {db_variable}")
                            else:
                                # seleccionar columna de valores: preferir la columna que coincida con data_key,
                                # si no existe, elegir la primera columna numérica distinta de lon/lat
                                value_col = None
                                if data_key in combined_df.columns:
                                    value_col = data_key
                                else:
                                    numeric_cols = combined_df.select_dtypes(include=['number']).columns.tolist()
                                    numeric_cols = [c for c in numeric_cols if c not in ('longitude', 'latitude')]
                                    if numeric_cols:
                                        value_col = numeric_cols[0]

                                if value_col:
                                    combined_df[value_col] = pd.to_numeric(combined_df[value_col], errors='coerce')
                                    # quitar NaN y ceros
                                    combined_df = combined_df.dropna(subset=[value_col])
                                    combined_df = combined_df[combined_df[value_col] != 0]
                                    z_values = combined_df[value_col].values
                                else:
                                    # no hay columna de valor numérica: usar 1s (pero también filtrar vacíos)
                                    z_values = np.ones(len(combined_df)) if not combined_df.empty else np.array([])

                                if combined_df.empty:
                                    print(f"⚠️ Sin valores válidos para {db_variable} después de filtrar 0/NaN")
                                else:
                                    gdf = gpd.GeoDataFrame(
                                        combined_df,
                                        geometry=gpd.points_from_xy(combined_df['longitude'], combined_df['latitude']),
                                        crs="EPSG:4326"
                                    )
                                    colorscale = request.POST.get('db_color', 'Turbo')
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

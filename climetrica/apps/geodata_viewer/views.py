from django.shortcuts import render

import plotly.express as px
import geopandas as gpd
from plotly.offline import plot

def map_view(request):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    fig = px.choropleth(world, geojson=world.geometry, locations=world.index, color='pop_est',
                        hover_name='name', projection='mercator',
                        title='World Population')
    plot_div = plot(fig, output_type='div')
    return render(request, 'templates/map.html', context={'plot_div': plot_div})


# Create your views here.

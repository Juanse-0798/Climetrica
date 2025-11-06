from django.urls import path
from .views import plot_map_view

urlpatterns = [
    path('map/', plot_map_view, name='map'),
]

from rest_framework.views import APIView
from rest_framework.response import Response
import plotly.graph_objs as go

class CapasAPIView(APIView):
    def get(self, request):
        # Simulación de capas cargadas desde memoria o base
        capas = [
            {
                "name": "temperatura del mar",
                "trace": go.Densitymapbox(
                    lat=[10, 11, 12],
                    lon=[-75, -74, -73],
                    z=[1, 2, 3],
                    radius=30,
                    colorscale="Turbo",
                    name="temperatura del mar",
                    showscale=False
                ).to_plotly_json()
            },
            {
                "name": "velocidad del viento",
                "trace": go.Densitymapbox(
                    lat=[10, 11, 12],
                    lon=[-75, -74, -73],
                    z=[3, 2, 1],
                    radius=30,
                    colorscale="Viridis",
                    name="velocidad del viento",
                    showscale=False
                ).to_plotly_json()
            }
        ]
        return Response(capas)

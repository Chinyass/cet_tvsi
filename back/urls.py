from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("get_traffic_ont",views.get_traffic_ont,name="ont_traffic")
]
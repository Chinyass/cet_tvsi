from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('ats',views.get_ats,name='ats')
]
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('ats',views.get_ats,name='ats'),
    path('find_ont',views.find_ont,name='find_ont'),
    path('setting_ont',views.setting_ont,name='setting_ont'),
    path('find_by_user',views.find_by_user,name='find_by_user')
]
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('ats',views.get_ats,name='ats'),
    path('find_ont',views.find_ont,name='find_ont'),
    path('setting_ont',views.setting_ont,name='setting_ont'),
    path('find_by_user',views.find_by_user,name='find_by_user'),
    path('get_nodes',views.get_nodes,name='get_nodes'),
    path('save_map',views.save_map,name='save_map'),
    path('search_vlan',views.search_vlan,name='search_vlan'),
    path('add_access_vlan',views.add_access_vlan,name='add_access_vlan'),
    path('add_trunk_vlans',views.add_trunk_vlans,name='add_trunk_vlans')
]
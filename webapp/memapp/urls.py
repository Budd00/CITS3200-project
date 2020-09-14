from django.urls import path
from django.conf.urls import url
from . import views, memdb

urlpatterns = [
   path('memdb/', views.hello),
    path('memdb/add_info', views.mod_memdb),
    path('memdb/add_detail',views.add_detail),
    path('memdb/getinfo',views.get_membership_data),
    path('memdb/getdetail',views.get_detail_data),
    path('memdb/delall',views.del_membership_data),
]
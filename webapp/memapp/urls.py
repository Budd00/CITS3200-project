from django.urls import path
from django.conf.urls import url
from . import views, memdb

urlpatterns = [
   path('', views.hello),
    path('memdb/add_info', memdb.mod_memdb),
    path('memdb/add_detail',views.add_detail),
    path('memdb/getall',memdb.get_membership_data),
    path('memdb/delall',memdb.del_membership_data),
]
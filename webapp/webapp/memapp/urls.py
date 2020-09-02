from django.urls import path
from django.conf.urls import url
from . import views, memdb

urlpatterns = [
   path('', views.hello),
    path('memdb/', memdb.mod_memdb),
    path('memdb/getall',memdb.get_membership_data),
    path('memdb/delall',memdb.del_membership_data),
]


from django.urls import path
from django.conf.urls import url
from . import views, memdb

urlpatterns = [
   path('', views.IndexView.as_view(), name='index'),
    path('add_info', views.mod_memdb),
    path('add_detail', views.add_detail),
    path('getinfo/<int:m_id>', views.get_membership_data, name="get_info"),
    path('getdetail/<int:m_id>', views.get_detail_data, name="get_detail"),
    path('delall', views.del_membership_data),
]
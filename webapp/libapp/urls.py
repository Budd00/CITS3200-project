from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-result/', views.search_result, name='search_result'),
    path('asset-entry/', views.asset_entry, name='asset_entry'),
    path('asset-entry/new-asset/', views.asset_entry, name='new_asset')
]

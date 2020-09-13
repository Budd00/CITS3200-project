from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/search-result/', views.search_result, name='search_result'),
    path('asset-create/', views.asset_create, name='asset_create'),
]

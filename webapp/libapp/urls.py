from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-result/', views.search_result, name='search_result')
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.refresh, name='home'),
    path('asset-create/', views.asset_create, name='asset_create'),
    path('tag-create/', views.tag_create, name='tag_create'),
    path('asset-edit/', views.asset_edit, name='asset_edit'),
    path('tag-link/', views.tag_link, name='tag_link'),
    path('delete/',views.asset_delete, name='asset_delete')
]

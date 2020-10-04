from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.refresh, name='home'),
    path('asset-create/', views.asset_create, name='asset_create'),
    path('tag-create/', views.tag_create, name='tag_create'),
    path('asset-edit/', views.asset_edit, name='asset_edit'),
    path('tag-link/', views.tag_link, name='tag_link'),
    path('tag-link/tag-unlink/', views.tag_unlink, name='tag_unlink'),
    path('tag-link/tag-add-child/', views.tag_add_child, name='tag-add-child'),
    path('tag-link/tag-edit/', views.tag_edit, name='tag_edit'),
    path('asset-delete/',views.asset_delete, name='asset_delete'),
    path('alt-delete/',views.alt_delete, name='alt_delete')
]

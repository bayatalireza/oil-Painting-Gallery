from django.urls import path
from . import views

app_name = 'artworks'

urlpatterns = [
    path('', views.artwork_list, name='list'),
    path('create/', views.artwork_create, name='create'),
    path('my/', views.my_artworks, name='my_list'),
    path('<slug:slug>/', views.artwork_detail, name='detail'),
    path('<slug:slug>/edit/', views.artwork_update, name='update'),
    path('<slug:slug>/delete/', views.artwork_delete, name='delete'),
]

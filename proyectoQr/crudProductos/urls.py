from django.urls import path
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.lista , name='gestionProductos'),
    path('registrarProducto/', views.registarProducto ),
    path('edicionProducto/editarProducto/', views.editarProducto,name='editarProducto'),
    path('edicionProducto/<codigo>', views.edicionProducto),
    path('eliminarProducto/<codigo>', views.eliminarProducto,name='eliminarProducto'),
    path('gestionProductos/registrarProducto/<codigo>', views.registarProducto),
    path('gestionProductos/eliminarProducto/<codigo>', views.eliminarProducto,name='eliminarProducto'),
   
    
]

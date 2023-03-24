from django.urls import path

from . import views

#url para la enlazar a la aplicacion generarQr
urlpatterns = [
    path('', views.generate, name='generarQr'),
]

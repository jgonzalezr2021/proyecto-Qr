from django.urls import path 
from . import views

#urls para la alimentacion dela camara.
urlpatterns=[
    path('', views.detect, name='detectarQr'),
    path('camera_feed', views.camera_feed, name='camera_feed'),
]
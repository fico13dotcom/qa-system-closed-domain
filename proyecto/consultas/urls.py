from django.urls import path
from consultas import views


urlpatterns = [
    path("", views.index, name="index"),
    path("subdominios", views.obtenerSubdominios, name="subdominios"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("libros/", views.lista_libros, name="lista-libros"),
    path("libros/<int:pk>/", views.libro_detail, name="libro-detail"),
    path("libros/agregar/", views.agregar_libro, name="agregar-libro"),
]

from django.shortcuts import render, get_object_or_404, redirect

from .models import Libro
from .forms import LibroForm


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, "actividadtesting/lista_libros.html", {"libros": libros})


def libro_detail(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, "actividadtesting/libro_detail.html", {"libro": libro})


def agregar_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista-libros")
    else:
        form = LibroForm()

    return render(request, "actividadtesting/agregar_libro.html", {"form": form})

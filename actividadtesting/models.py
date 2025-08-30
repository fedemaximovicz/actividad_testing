from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_year(value):
    current_year = timezone.now().year
    if value < 1 or value > current_year:
        raise ValidationError(f"El año tiene que ser entre 1 y el año actual: {current_year}.")


class Autor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")
    descripcion = models.TextField(blank=True, max_length=600)
    publicacion_year = models.PositiveBigIntegerField(validators=[validate_year])
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
    

    


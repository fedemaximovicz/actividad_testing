from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Autor, Libro
from .forms import LibroForm


# ----------------------------
# Model Tests
# ----------------------------
class AutorModelTest(TestCase):
    def test_str_returns_nombre(self):
        autor = Autor.objects.create(nombre="Gabriel García Márquez")
        self.assertEqual(str(autor), "Gabriel García Márquez")


class LibroModelTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Julio Cortázar")

    def test_str_returns_titulo_and_autor(self):
        libro = Libro.objects.create(
            titulo="Rayuela", autor=self.autor, publicacion_year=1963
        )
        self.assertEqual(str(libro), "Rayuela - Julio Cortázar")

    def test_publicacion_year_validator_future(self):
        future_year = timezone.now().year + 10
        libro = Libro(
            titulo="Libro del Futuro",
            autor=self.autor,
            publicacion_year=future_year,
        )
        with self.assertRaises(ValidationError):
            libro.full_clean()  # triggers model validation

    def test_publicacion_year_validator_negative(self):
        libro = Libro(
            titulo="Libro Antiguo",
            autor=self.autor,
            publicacion_year=-500,
        )
        with self.assertRaises(ValidationError):
            libro.full_clean()


# ----------------------------
# Form Tests
# ----------------------------
class LibroFormTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Isabel Allende")

    def test_valid_form(self):
        current_year = timezone.now().year
        form = LibroForm(
            data={
                "titulo": "La Casa de los Espíritus",
                "autor": self.autor.id,
                "publicacion_year": current_year,
                "disponible": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_future_year(self):
        future_year = timezone.now().year + 5
        form = LibroForm(
            data={
                "titulo": "Libro del Futuro",
                "autor": self.autor.id,
                "publicacion_year": future_year,
                "disponible": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("publicacion_year", form.errors)


# ----------------------------
# View Tests
# ----------------------------
class LibroViewTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Jorge Luis Borges")
        self.libro = Libro.objects.create(
            titulo="Ficciones", autor=self.autor, publicacion_year=1944
        )

    def test_lista_libros_view(self):
        response = self.client.get(reverse("lista-libros"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "actividadtesting/lista_libros.html")
        self.assertContains(response, "Ficciones")

    def test_libro_detail_view(self):
        response = self.client.get(reverse("libro-detail", args=[self.libro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "actividadtesting/libro_detail.html")
        self.assertContains(response, "Ficciones")

    def test_agregar_libro_view_post_valid(self):
        response = self.client.post(
            reverse("agregar-libro"),
            {
                "titulo": "El Aleph",
                "autor": self.autor.id,
                "publicacion_year": 1949,
                "disponible": True,
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to lista-libros
        self.assertEqual(Libro.objects.count(), 2)

    def test_agregar_libro_view_post_invalid(self):
        future_year = timezone.now().year + 5
        response = self.client.post(
            reverse("agregar-libro"),
            {
                "titulo": "Libro Inválido",
                "autor": self.autor.id,
                "publicacion_year": future_year,  # invalid
                "disponible": True,
            },
        )
        self.assertEqual(response.status_code, 200)  # stays on form page
        self.assertTemplateUsed(response, "actividadtesting/agregar_libro.html")
        self.assertEqual(Libro.objects.count(), 1)  # still only 1 valid book

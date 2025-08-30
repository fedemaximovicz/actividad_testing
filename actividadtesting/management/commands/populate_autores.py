
from django.core.management.base import BaseCommand

from actividadtesting.models import Autor

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):


        autores = [
            Autor(nombre="Cacho Randomniano"),
            Autor(nombre="Isaac Asimov"),
            Autor(nombre="H.G Wells"),
            Autor(nombre="Aurthur Conan Doyle"),
            Autor(nombre="Jorge Luis Borges"),
            Autor(nombre="Charles Dickens"),
            Autor(nombre="Emily Bronte"),
            Autor(nombre="Julio Cortazar"),
            Autor(nombre="J.K Rowlings"),
        ]


        Autor.objects.bulk_create(autores)

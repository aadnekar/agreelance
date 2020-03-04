import os
import factory
from factory.django import DjangoModelFactory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreelance.settings')
import django
django.setup()

from projects.models import ProjectCategory


class ProjectCategoryFactory(DjangoModelFactory):

    class Meta:
        model = ProjectCategory

    name = factory.Iterator(["Cleaning", "Painting", "Gardening"])
import factory
from factory.django import DjangoModelFactory
from projects.models import Project

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    
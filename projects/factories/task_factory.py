import os
import factory
from factory.django import DjangoModelFactory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreelance.settings')
import django
django.setup()

from projects.models import Task

from projects.factories.project_factory import ProjectFactory

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task


    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: f"Some Task Title {n}")
    description = "Some description"
    budget = 0

    status = Task.AWAITING_DELIVERY
    feedback = "Some feedback"
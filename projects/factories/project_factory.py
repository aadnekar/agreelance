import os
import factory
from factory.django import DjangoModelFactory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreelance.settings')
import django
django.setup()

from projects.models import Project
from projects.factories.project_category_factory import ProjectCategoryFactory
from user.factories.profile_factory import ProfileFactory

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    user = factory.SubFactory(ProfileFactory)
    title = factory.Sequence(lambda n: f"Title {n}")
    description = "Some Description"

    category = factory.SubFactory(ProjectCategoryFactory)


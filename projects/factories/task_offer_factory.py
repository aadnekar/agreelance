import os
import factory
from factory.django import DjangoModelFactory
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agreelance.settings")
import django
django.setup()

from projects.models import TaskOffer

from projects.factories.task_factory import TaskFactory
from user.factories.profile_factory import ProfileFactory


class TaskOfferFactory(DjangoModelFactory):

    class Meta:
        model = TaskOffer

    task = factory.SubFactory(TaskFactory)
    offerer = factory.SubFactory(ProfileFactory)
    title = "Some Title"
    description = "Some Description"
    price = 0

import os
import factory
from factory.django import DjangoModelFactory
# from user.models import Profile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreelance.settings')
import django
django.setup()

from django.contrib.auth.models import User

# @factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    """
    The UserFactory is a utility class to be used when testing the application.
    A simple instansiation of the class will save the a user object in the
    testing database. e.g.
    user = UserFactory() --> creates and saves a user.
    user = UserFactory().build() --> creates a user without saving it.
    user = UserFactory(is_staff=True, is_superuser=True) --> creates a superuser
    """
    class Meta:
        model = User

    first_name = factory.Faker('first_name', locale='no_NO')
    last_name = factory.Faker('last_name', locale='no_NO')

    username = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}{o.last_name[:3].lower()}")

    # is_staff == False
    # is_superuser == False
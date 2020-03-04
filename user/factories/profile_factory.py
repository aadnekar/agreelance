import os
import factory
from factory.django import DjangoModelFactory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreelance.settings')
import django
django.setup()

from user.models import Profile
from user.factories.user_factory import UserFactory

class ProfileFactory(DjangoModelFactory):
    """
    The ProfileFactory is a utility class to be used when testing the application.
    A simple instansiation of the class will save the a user object in the
    testing database. e.g.
    """
    class Meta:
        model = Profile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    company = 'The Company'
    phone_number = '00000000'
    country = factory.Faker('country')
    # Should be given someting appropriate to the country
    state = factory.Faker('state')
    city = factory.Faker('city')
    postal_code = factory.Faker('postalcode')
    street_address = factory.Faker('street_address')

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            print(f"EXTRACTED = {extracted}")
            # A list of categories were passed in, add them.
            for category in extracted:
                self.categories.add(category)

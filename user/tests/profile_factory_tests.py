import pytest

from user.factories.profile_factory import ProfileFactory
from user.factories.user_factory import UserFactory
from projects.factories.project_category_factory import ProjectCategoryFactory


# @pytest.fixture
# def profile():
#     return ProfileFactory

# @pytest.mark.django_db
# def test_profile_factory_creates_a_user():
#     """
#     A ProfileFactory should automatically create a UserFactory using the
#     SubFactory attribute.
#     """
#     profile = ProfileFactory()

#     assert profile.user is not None

@pytest.fixture()
def cleaning_category():
    return ProjectCategoryFactory(name="Cleaning")


@pytest.fixture()
def painting_category():
    return ProjectCategoryFactory(name="Painting")


@pytest.fixture()
def gardening_category():
    return ProjectCategoryFactory(name="Gardening")


@pytest.mark.django_db
def test_that_profile_contains_two_categories(cleaning_category, painting_category):

    profile = ProfileFactory.create(categories=(cleaning_category, painting_category))

    for category in profile.categories.all():
        assert str(category) in ("Cleaning", "Painting")


@pytest.mark.django_db
def test_that_profile_contains_three_categories(
    cleaning_category, painting_category, gardening_category):

    profile = ProfileFactory.create(categories=(
        cleaning_category, painting_category, gardening_category
    ))

    for category in profile.categories.all():
        assert str(category) in ("Cleaning", "Painting", "Gardening")


# @pytest.mark.django_db
# def test_profile_displays_appropriate_company_name(profile):
#     """
#     A profile should have a company displayed. The ProfileFactory displays the
#     last name of the user associated to the profile with an ASA ending.
#     """

#     assert isinstance(profile.company, str)
#     assert len(profile.company) >= 5

# @pytest.mark.django_db
# def test_profile_displays_appropriate_norwegian_phone_number(profile):
#     """
#     A ProfileFactory should make a fake norwegian phone number
#     """

#     print(profile.phone_number)
#     assert isinstance(profile.phone_number, str)
#     assert len(profile.phone_number) == 8

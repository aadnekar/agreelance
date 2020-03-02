import pytest

from user.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_user_is_assigned_first_and_last_name_successfully():
    """ A user should be assigned a first name and last name """

    # Return a user instance without saving it to save time.
    user = UserFactory()

    assert user.first_name is not None and user.last_name is not None



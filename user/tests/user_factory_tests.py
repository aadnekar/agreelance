import pytest

from user.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_user_is_assigned_first_and_last_name_successfully():
    """ A user should be assigned a first name and last name """

    # Return a user instance without saving it to save time.
    user = UserFactory.build()

    assert user.first_name is not None and user.last_name is not None


@pytest.mark.django_db
def test_that_two_different_users_have_different_names():
    user1 = UserFactory.build()
    user2 = UserFactory.build()

    assert (
        user1.first_name + " " + user1.last_name
        != user2.first_name + " " + user2.last_name
    )


@pytest.mark.django_db
def test_first_and_last_name_may_be_set_manually():
    user = UserFactory(first_name="Ådne", last_name="Karstad")

    assert user.first_name == "Ådne"
    assert user.last_name == "Karstad"


@pytest.mark.django_db
def test_username_is_set_automatically():
    user = UserFactory.build()

    assert user.username is not None


@pytest.mark.django_db
def test_user_name_is_correct():
    """
    The username should be the first name pluss the three first characters
    in the last name, all in lowercase.
    """
    user = UserFactory.build()
    expected = user.first_name.lower() + user.last_name[:3].lower()

    assert user.username == expected


# @pytest.mark.django_db
# def test_user_is_not_staff_and_is_not_superuser():
#     """ By default a user should neither be staff nor superuser """
#     user = UserFactory

#     assert user.is_superuser is not True

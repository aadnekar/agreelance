import pytest
from pytest_django.asserts import assertRedirects

from django.test import Client

from user.factories.profile_factory import ProfileFactory


@pytest.fixture
def client():
    """ Creates a django test client and returns it """
    return Client()

@pytest.fixture
def user():
    """ Creates a connected Profile and User and returns the profile """
    return ProfileFactory()


@pytest.mark.django_db
def test_that_unauthorized_users_do_not_get_error_on_profile_request(client):
    """
    A user should get a status code of 200 OK if they are able to make a request
    to /user/profile/ because they should be redirected to some other page.
    """

    response = client.get("/user/profile/", follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_that_unauthorized_users_are_redirected(client):
    """ A user who has not logged in should be redirected to a signup page """

    expected_url = "/user/signup/"
    response = client.get("/user/profile/", follow=True)

    assertRedirects(response, expected_url)


@pytest.mark.django_db
def test_authorized_users_may_access_their_profile_page(client, user):
    "A user should recieve a status code 200 OK when they request their profile"

    client.force_login(user.user)

    response = client.get("/user/profile/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_authorized_users_may_access_their_profile_page(client, user):
    """
    The profile page should return the current users username, and definetly
    not someone elses username
    """
    client.force_login(user.user)

    response = client.get("/user/profile/")

    assert response.context['user'].username == user.user.username

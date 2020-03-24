import pytest
from pytest_django.asserts import assertRedirects
from user.models import Profile
from user.factories.profile_factory import ProfileFactory

from django.test import Client

@pytest.fixture
def client():
    """ Creates a django test client and returns it """
    return Client()

@pytest.fixture
def profile():
    """ Returns a user profile """
    return ProfileFactory()

@pytest.mark.django_db
def test_boundary_values(client):
    data = {
        'username': 'user',
        'first_name': 'User',
        'last_name': 'Userson',
        'categories': 1,
        'company': 'company',
        'email': 'user@email.com',
        'email_confirmation': 'user@email.com',
        'password1': '123pass456',
        'password2': '123pass456',
        'phone_number': '12345678',
        'country': 'country',
        'state': 'state',
        'city': 'city',
        'postal_code': '1234',
        'street_address': 'street'
    }

    # Test username: 0 characters, 149, 150, 151
    username_values = [0, 149, 150, 151]
    for value in username_values:
        new_data = data
        new_data['username'] = 's' * value
        response = client.post(f"/user/signup/", data=new_data)
        users = Profile.objects.all()
        assert response.status_code == 200
        assert len(users) == 0

    # Test first name: 0 characters, 1, 99999
    first_name_values = [0, 1, 99999]
    for value in first_name_values:
        new_data = data
        new_data['first_name'] = 's' * value
        response = client.post(f"/user/signup/", data=new_data)
        users = Profile.objects.all()
        assert response.status_code == 200
        assert len(users) == 0
    
    # Test password: 0 characters, 7, 8, 9
    password_values = [0, 7, 8, 9]
    for value in password_values:
        new_data = data
        new_data['password1'] = 's' * value
        new_data['password2'] = 's' * value
        response = client.post(f"/user/signup/", data=new_data)
        users = Profile.objects.all()
        assert response.status_code == 200
        assert len(users) == 0

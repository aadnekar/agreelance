import pytest

from django.test import Client




@pytest.fixture
def client():
    return Client()


@pytest.fixture
def profile():
    """ Returns a user profile """
    return ProfileFactory()


@pytest.fixture
def task():
    """ Returns a task """
    return TaskFactory()





def test_user_with_only_read_permission_is_redirected():
    pass
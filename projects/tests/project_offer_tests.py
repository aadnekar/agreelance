import pytest
from pytest_django.asserts import assertRedirects
from user.models import Profile
from user.factories.profile_factory import ProfileFactory
from projects.factories.task_offer_factory import TaskOfferFactory
from projects.factories.project_factory import ProjectFactory
from projects.factories.task_factory import TaskFactory
from django.test import Client
from projects.models import (
    Project,
    TaskOffer,
)

@pytest.fixture
def client():
    """ Creates a django test client and returns it """
    return Client()

@pytest.fixture
def project():
    """ Returns a project """
    return ProjectFactory()

@pytest.fixture
def profile():
    """ Returns a user profile """
    return ProfileFactory()

@pytest.mark.django_db
def test_boundary_values(client, project, profile):
    # Create a task for the specified project
    task = TaskFactory(project=project, budget=200)

    # Login as a user
    client.force_login(profile.user)

    # Make a post request to make an offer to the specified task
    data = {
        "title": "My offer",
        "description": "Yes we can!",
        "price": 150,
    }

    # Test title: 0, 199, 200, 201 characters
    title_values = [0, 199, 200, 201]
    for value in title_values:
        new_data = data
        new_data['title'] = 's' * value
        response = client.post(f"/projects/{project.id}/", data=new_data)
        task_offers = TaskOffer.objects.all()
        assert response.status_code == 200
        assert len(task_offers) == 0

    # Test description: 0 characters
    new_data = data
    new_data['description'] = ''
    response = client.post(f"/projects/{project.id}/", data=new_data)  
    task_offers = TaskOffer.objects.all()
    assert response.status_code == 200
    assert len(task_offers) == 0

    #Test price: -1, 0, 1
    price_values = [-1, 0, 1]
    for value in price_values:
        new_data = data
        new_data['price'] = value
        response = client.post(f"/projects/{project.id}/", data=new_data)
        task_offers = TaskOffer.objects.all()
        assert response.status_code == 200
        assert len(task_offers) == 0

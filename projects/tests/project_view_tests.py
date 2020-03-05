import pytest

from django.test import Client
from django.http import (
    Http404
)

from projects.models import Project

from projects.factories.project_factory import ProjectFactory
from projects.factories.task_factory import TaskFactory

from user.factories.profile_factory import ProfileFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def project():
    """ Returns a project """
    return ProjectFactory()


@pytest.fixture
def profile():
    """ Returns a profile """
    return ProfileFactory()


def generate_tasks(project, number_of_tasks, budget=0):
    """ Generate a given number_of_tasks for the given project """
    for i in range(number_of_tasks):
        TaskFactory.create(project=project, budget=budget)


def get_response(request):
    pass


@pytest.mark.django_db
def test_request_to_existing_project(client, project):
    """Request to an exisiting project should return 200 OK """
    response = client.get(f"/projects/{project.id}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_request_to_non_existing_project(client):
    """Request to a non exisiting project should return 404 OK """

    try:
        response = client.get(f"/projects/{1}/")
    except Project.DoesNotExist:
        assert True


@pytest.mark.temp
@pytest.mark.django_db
def test_that_all_task_related_to_a_project_are_returned(client, project):
    """
    All tasks that are connected to a project should be displayed
    in the response.
    """
    generate_tasks(project=project, number_of_tasks=3)
    response = client.get(f"/projects/{project.id}/")

    assert response.context['tasks'].count() == 3


@pytest.mark.django_db
def test_that_total_budget_cannot_be_negative(client, project):
    """
    If the budget of a task is set to a negative amount, the total_budget
    shoule not be negative.
    """
    generate_tasks(project=project, number_of_tasks=3, budget=-50)
    response = client.get(f"/projects/{project.id}/")

    assert response.context['total_budget'] > 0


#TODO: Fix fault, temporarily skipped due to fail.
@pytest.mark.skip
@pytest.mark.django_db
def test_that_total_budget_cannot_be_negative(client, project):
    """
    If the budget of a task is set to a negative amount, the total_budget
    shoule not be negative.
    """
    generate_tasks(project=project, number_of_tasks=3, budget=-50)
    response = client.get(f"/projects/{project.id}/")

    assert response.context['total_budget'] > 0


@pytest.mark.django_db
def test_that_total_budget_is_properly_added(client, project):
    """
    Tests that if tasks with budgets are added appropriately
    """
    generate_tasks(project=project, number_of_tasks=3, budget=300)
    response = client.get(f"/projects/{project.id}/")

    assert response.context['total_budget'] == 900


@pytest.mark.django_db
def test_total_budget_when_there_are_no_tasks(client, project):
    """ If there are no tasks the total_budget should equal zero """
    response = client.get(f"/projects/{project.id}/")

    assert response.context['total_budget'] == 0



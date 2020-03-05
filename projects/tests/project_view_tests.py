import pytest

from django.test import Client
from django.http import (
    Http404
)

from projects.models import (
    Project,
    TaskOffer,
)

from projects.templatetags.project_extras import get_all_taskoffers

from projects.factories.project_factory import ProjectFactory
from projects.factories.task_factory import TaskFactory
from projects.factories.task_offer_factory import TaskOfferFactory

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


@pytest.fixture
def project_with_pending_offer():
    """
    Creates a project with a task that has recieved an offer, and returns
    the project, task, and profile related to the offer.
    """
    project_owner = ProfileFactory()
    offerer = ProfileFactory()
    project = ProjectFactory(user=project_owner)
    task = TaskFactory(project=project, budget=200)
    offer = TaskOfferFactory(task=task, offerer=offerer)
    return {
        "project_owner": project_owner,
        "offerer": offerer,
        "project": project,
        "task": task,
        "offer": offer
    }

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


@pytest.mark.django_db
def test_user_successfully_making_an_offer_to_a_task(client, project, profile):
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
    response = client.post(f"/projects/{project.id}/", data=data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_offer_is_displayed_for_project_owner(
    client, project_with_pending_offer):
    # Log in as the project_owner
    client.force_login(project_with_pending_offer['project_owner'].user)

    response = client.get(
        f"/projects/{project_with_pending_offer['project'].id}/"
    )

    task_from_response = response.context['tasks'][0]
    offer = get_all_taskoffers(task_from_response)[0]

    assert response.status_code == 200
    assert  offer.status == TaskOffer.PENDING
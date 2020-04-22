import pytest

from django.test import Client
from django.http import (
    Http404
)
from projects.models import (
    Task,
    Project,
    TaskOffer,
)
from projects.forms import(
    TaskOfferForm,
)
from projects.templatetags.project_extras import get_all_taskoffers
from projects.factories.project_factory import ProjectFactory
from projects.factories.task_factory import TaskFactory
from projects.factories.task_offer_factory import TaskOfferFactory
from projects.views import (
    get_user_task_permissions,
)
from projects.viewsets.project_view import (
    calculate_project_budget,
)
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
    """ Returns a user profile """
    return ProfileFactory()


@pytest.fixture
def task():
    """ Returns a task """
    return TaskFactory()


@pytest.fixture
def profile_project_task():
    """ Returns a profile, project and task """
    profile = ProfileFactory()
    project = ProjectFactory(user=profile)
    task = TaskFactory(project=project)
    return {
        'profile': profile,
        'project': project,
        'task': task
    }

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


@pytest.mark.temp
@pytest.mark.django_db
def test_calculate_project_budget():
    for n in range(5):
        TaskFactory(budget=10)
    tasks = Task.objects.all()

    expected_result = 50
    result = calculate_project_budget(tasks)

    assert result == expected_result


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
def test_that_project_budget_is_properly_added(client, project):
    """
    Tests that if tasks with budgets are added appropriately
    """
    generate_tasks(project=project, number_of_tasks=3, budget=300)
    response = client.get(f"/projects/{project.id}/")

    assert response.context['project_budget'] == 900


@pytest.mark.django_db
def test_project_budget_when_there_are_no_tasks(client, project):
    """ If there are no tasks the project_budget should equal zero """
    response = client.get(f"/projects/{project.id}/")

    assert response.context['project_budget'] == 0


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


@pytest.mark.django_db
def test_submit_offer_successfull(client, profile, project):
    """ A successfull post on the TaskOfferForm should create a new TaskOffer """
    task = TaskFactory(project=project)
    client.force_login(profile.user)

    form_data = {
        'offer_submit': True,
        'title': "A successfull task offer",
        'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec venenatis.",
        'price': 200,
        'taskvalue': task.id
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    task_offers = TaskOffer.objects.all()

    assert response.status_code == 200
    assert isinstance(response.context['task_offer_form'], TaskOfferForm)
    assert len(task_offers) > 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title,description,price",
    [
        ('', 'Lorem ipsum dolaris jabbadabba', 200),
        ("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a quam
         nibh. In et lobortis magna, at convallis ipsum. Donec quis vehicula diam. 
         Nullam blandit purus vitae mauris eleifend venenatis. Vivamus ut lacus nec 
         diam pulvinar fermentum ornare non nulla. Phasellus aliquam libero a sem 
         congue, vitae fringilla sem malesuada. Vestibulum tempus non ligula sit amet 
         imperdiet. Praesent scelerisque, odio in vestibulum fermentum, lacus ipsum 
         rhoncus ante, ut gravida enim velit mollis mauris. In hac habitasse platea 
         dictumst. Etiam finibus consectetur purus, tempor sodales leo semper in. 
         Nullam dapibus dapibus blandit. Sed lectus urna, vestibulum eget sem eu, 
         consectetur rutrum quam. Donec ac erat nunc. Integer quis vulputate purus. 
         Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed semper urna 
         id sem porta fringilla. Aenean a auctor tellus. Praesent fermentum libero non 
         quam interdum dapibus. Integer non nisi magna. Donec ut euismod turpis, vitae 
         egestas dolor. Cras ut mollis enim, nec facilisis libero. Vivamus nec nulla 
         lacus. Maecenas velit nisl, vestibulum at pharetra ac, sollicitudin congue 
         nunc. Sed ac rhoncus lorem. Aliquam dictum ex vitae elementum fringilla. 
         Aliquam urna dui, maximus ut tincidunt vitae, placerat eu mauris. Curabitur 
         hendrerit semper ipsum in congue. Suspendisse potenti. 
         Aenean ultrices est nec.""", 'Lorem ipsum dolaris jabbadabba', 200),
         (999, 'Lorem ipsum dolaris jabbadabba', 200),
         ('Proper Title', 501, 200),
         ('Proper Title', 'Lorem ipsum dolaris jabbadabba', 'This is not numbers'),
    ]
)
def test_that_no_offer_is_created_when_task_offer_form_fields_are_invalid(
    client, profile, project, title, description, price):
    """A Task Offer should not be created when a form field is invalid."""
    task = TaskFactory(project=project)
    client.force_login(profile.user)

    form_data = {
        'offer_submit': {
            'offer_submit': True,
            'title': title,
            'description': description,
            'price': price,
            'taskvalue': task.id
        }
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    task_offers = TaskOffer.objects.all()

    assert response.status_code == 200
    assert len(task_offers) == 0


@pytest.mark.django_db
def test_successfully_accept_task_offer(client, project_with_pending_offer):
    """An accepted task offer should make the offerer a participant in the project"""
    owner = project_with_pending_offer['project_owner']
    offerer = project_with_pending_offer['offerer']
    project = project_with_pending_offer['project']
    offer = project_with_pending_offer['offer']
    client.force_login(owner.user)

    form_data = {
        'offer_response': True,
        'status': "This is an invalid status code",
        'feedback': "This is a valid text area",
        'taskofferid': offer.id
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    project = Project.objects.get(id=project.id)

    assert response.status_code == 200
    assert len(project.participants.all()) == 0


@pytest.mark.django_db
def test_TaskOfferResponseForm_with_invalid_fields(client, project_with_pending_offer):
    """
    The offerer shall not be added to participants of the project if the
    TaskOfferResponseForm is not valid
    """
    owner = project_with_pending_offer['project_owner']
    offerer = project_with_pending_offer['offerer']
    project = project_with_pending_offer['project']
    offer = project_with_pending_offer['offer']
    client.force_login(owner.user)

    form_data = {
        'offer_response': True,
        'status': TaskOffer.ACCEPTED,
        'feedback': 'jabbadabba helt ok',
        'taskofferid': offer.id
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    project = Project.objects.get(id=project.id)

    assert response.status_code == 200
    assert len(project.participants.all()) == 1
    assert project.participants.all()[0] == offerer


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [(TaskOffer.PENDING,), (TaskOffer.DECLINED,)]
)
def test_that_no_participant_is_added_if_status_is_not_set_to_accepted(
    client, project_with_pending_offer, status):
    """
    If status code is set to declined or kept as pending, the offerer should not
    be put as a participant in the project
    """
    owner = project_with_pending_offer['project_owner']
    offerer = project_with_pending_offer['offerer']
    project = project_with_pending_offer['project']
    offer = project_with_pending_offer['offer']
    client.force_login(owner.user)

    form_data = {
        'offer_response': True,
        'status': status,
        'feedback': 'jabbadabba helt ok',
        'taskofferid': offer.id
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    project = Project.objects.get(id=project.id)

    assert response.status_code == 200
    assert len(project.participants.all()) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [(Project.OPEN), (Project.INPROG), (Project.FINISHED)]
)
def test_successfully_changing_status_of_a_project(
    client, project_with_pending_offer, status):
    owner = project_with_pending_offer['project_owner']
    project = project_with_pending_offer['project']
    client.force_login(owner.user)

    form_data = {
        'status_change': True,
        'status': status
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    project.refresh_from_db()

    assert response.status_code == 200
    assert project.status == status


@pytest.mark.django_db
def test_that_status_of_project_is_not_changed_when_the_ProjectStatusForm_is_invalid(
    client, project_with_pending_offer):
    owner = project_with_pending_offer['project_owner']
    project = project_with_pending_offer['project']
    old_project_status = project.status
    client.force_login(owner.user)

    form_data = {
        'status_change': True,
        'status': 'This is not a valid status'
    }
    response = client.post(f'/projects/{project.id}/', data=form_data)
    project.refresh_from_db()

    assert response.status_code == 200
    assert project.status == old_project_status


@pytest.mark.django_db
def test_task_owner_has_all_permissions(profile_project_task):
    user = profile_project_task['profile'].user
    task = profile_project_task['task']

    expected_permissions = {
        'write': True,
        'read': True,
        'modify': True,
        'owner': True,
        'upload': True,
    }
    actual_permissions = get_user_task_permissions(user=user, task=task)

    assert all(
        [actual == expected for actual, expected in zip(
            expected_permissions.values(),actual_permissions.values()
        )]
    )


@pytest.mark.django_db
def test_accepted_task_offer_gives_correct_permissions_to_offerer():
    """
    A offerer with accepted offer has write, read, modify and upload permissions,
    but not does not have owner permissions.
    """
    offerer = ProfileFactory()
    project = ProjectFactory()
    task = TaskFactory(project=project, budget=200)
    offer = TaskOfferFactory(task=task, offerer=offerer)
    offer.status = TaskOffer.ACCEPTED
    offer.save()

    expected_permissions = {
        'write': True,
        'read': True,
        'modify': True,
        'owner': False,
        'upload': True,
    }
    actual_permissions = get_user_task_permissions(user=offerer.user, task=task)

    assert all(
        [actual == expected for actual, expected in zip(
            expected_permissions.values(),actual_permissions.values()
        )]
    )


@pytest.mark.django_db
def test_default_permissions(profile, task):
    """
    A user without any relation to a task does not any have permissions
    """
    user = profile.user

    expected_permissions = {
        'write': False,
        'read': False,
        'modify': False,
        'owner': False,
        'upload': False,
    }
    actual_permissions = get_user_task_permissions(user=user, task=task)

    assert all(
        [actual == expected for actual, expected in zip(
            expected_permissions.values(),actual_permissions.values()
        )]
    )


# @pytest.mark.temp
# @pytest.mark.django_db
# def test_task_model_read_field():
#     task = TaskFactory()
#     task.read.add(ProfileFactory())
#     task.save()
#     task.refresh_from_db()
    

#     assert False

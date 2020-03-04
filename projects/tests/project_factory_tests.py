import pytest

from projects.factories.project_factory import ProjectFactory
from projects.models import Project


@pytest.fixture
def project():
    return ProjectFactory()


@pytest.mark.django_db
def test_project_factory_creates_a_new_user(project):

    assert project.user is not None


@pytest.mark.django_db
def test_project_has_default_status(project):

    assert project.status == Project.OPEN


@pytest.mark.django_db
def test_that_it_is_possible_to_make_project_with_finished_status():

    finished_project = ProjectFactory(status=Project.FINISHED)

    assert finished_project.status == Project.FINISHED
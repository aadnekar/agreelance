import pytest

from projects.models import Task
from projects.factories.task_factory import TaskFactory
from projects.factories.project_factory import ProjectFactory


@pytest.fixture
def task():
    return TaskFactory()


@pytest.fixture
def project():
    return ProjectFactory()


@pytest.mark.django_db
def test_that_task_factory_creates_a_default_project(task):

    assert task.project is not None


@pytest.mark.django_db
def test_that_task_factory_can_be_assigned_a_specific_project(project):
    task = TaskFactory(project=project)

    assert task.project == project

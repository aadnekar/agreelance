from django.shortcuts import get_object_or_404, render

from projects.forms import (ProjectStatusForm, TaskOfferForm,
                            TaskOfferResponseForm)
from projects.models import Delivery, Project, Task, TaskOffer


def project_view(request, project_id):
    """ Displays a given project """

    project = Project.objects.get(pk=project_id)
    tasks = project.tasks.all()
    project_budget = calculate_project_budget(tasks)

    if user_is_project_owner(request.user, project):
        return display_project_view_for_project_owner(
            request, project, tasks, project_budget
        )
    else:
        return display_project_view_for_default_user(
            request, project, tasks, project_budget
        )


def calculate_project_budget(tasks):
    """ Calculates a total budget from a set of tasks """
    result = 0
    for task in tasks:
        result += task.budget

    return result


def user_is_project_owner(user, project):
    """ Checks if the user is the owner of the project """
    return user == project.user.user


def display_project_view_for_project_owner(
        request, project, tasks, project_budget):
    """ Return the project_view appropriate for the project owner """
    if task_offer_response_form_prompted(request):
        display_task_offer_response_form(request)

    if project_status_form_is_prompted(request):
        display_project_status_form(request, project)

    offer_response_form = TaskOfferResponseForm()
    status_form = ProjectStatusForm(initial={"status": project.status})

    return render(
        request,
        "projects/project_view.html",
        {
            "project": project,
            "tasks": tasks,
            "status_form": status_form,
            "project_budget": project_budget,
            "offer_response_form": offer_response_form,
        },
    )


def display_project_view_for_default_user(
        request, project, tasks, project_budget):
    """ Return the default project view """
    if task_offer_submission_form_is_prompted(request):
        display_task_offer_submission_form(request)

    task_offer_form = TaskOfferForm()

    return render(
        request,
        "projects/project_view.html",
        {
            "project": project,
            "tasks": tasks,
            "task_offer_form": task_offer_form,
            "project_budget": project_budget,
        },
    )


def give_task_read_permission_to_new_participant(task, participant):
    """ Give a specified user (participant) read access to a specified task """
    task.read.add(participant)


def give_task_write_permission_to_new_participant(task, participant):
    """ Give a specified user (participant) write access to a specified task """
    task.write.add(participant)


def give_task_read_and_write_permission_to_new_participant(task, participant):
    """
    Give a specified user (participant) read and write access
    to a specified task
    """
    give_task_read_permission_to_new_participant(task, participant)
    give_task_write_permission_to_new_participant(task, participant)


def add_new_participant_to_project(project, new_participant):
    """ Add a specified user to the participants list in a specified project """
    project.participants.add(new_participant)


def project_status_form_is_prompted(request):
    """ Checks if the request prompts for a status form to be displayed """
    return request.method == "POST" and "status_change" in request.POST


def display_project_status_form(request, project):
    """ Display the project status form to the project owner """
    status_form = ProjectStatusForm(request.POST)
    if status_form.is_valid():
        project_status = status_form.save(commit=False)
        project.status = project_status.status
        project.save()


def task_offer_response_form_prompted(request):
    """
    Checks if the request prompts for an offer response form to be displayed
    """
    return request.method == "POST" and "offer_response" in request.POST


def display_task_offer_response_form(request):
    """ Display the task offer response form to the project owner """
    instance = get_object_or_404(TaskOffer, id=request.POST.get("taskofferid"))
    offer_response_form = TaskOfferResponseForm(request.POST, instance=instance)
    if offer_response_form.is_valid():
        offer_response = offer_response_form.save(commit=False)
        if offer_response.status == Delivery.ACCEPTED:
            give_task_read_and_write_permission_to_new_participant(
                offer_response.task, offer_response.offerer)
            add_new_participant_to_project(
                offer_response.task.project, offer_response.offerer)
        offer_response.save()


def task_offer_submission_form_is_prompted(request):
    """
    Checks if the request prompts for an offer submission form to be displayed
    """
    return request.method == "POST" and "offer_submit" in request.POST


def display_task_offer_submission_form(request):
    """ Displays the task offer submission form """
    task_offer_form = TaskOfferForm(request.POST)
    if task_offer_form.is_valid():
        task_offer = task_offer_form.save(commit=False)
        task_offer.task = Task.objects.get(pk=request.POST.get("taskvalue"))
        task_offer.offerer = request.user.profile
        task_offer.save()

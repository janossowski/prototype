from django.shortcuts import get_object_or_404, render, redirect
from project.models import Project
from comment.models import Comment
from task.models import Task
from need.models import Need
from django.urls import path, reverse
from django.db.models import Prefetch


def index(request):
    """
    Display a list of the latest projects.
    """
    latest_projects_list = Project.objects.order_by('id')
    context = {
        "latest_projects_list": latest_projects_list,
    }
    return render(request, "index.html", context=context)


def project(request, project_id):
    """
    Display the project details along with its needs and comments.
    """
    project = get_object_or_404(Project, pk=project_id)
    needs = Need.objects.filter(to_project=project)  # Assuming `to_project` is the FK in Need
    comments = project.comments.filter(parent__isnull=True)  # Top-level comments only

    context = {
        "content": project,
        "needs": needs,
        "comments": comments,
    }
    return render(request, "details.html", context)

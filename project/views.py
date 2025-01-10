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
    content = get_object_or_404(Project, pk=project_id)

    # Get related needs
    needs = content.need_set.all()  # Assuming a reverse relation from Project to Need

    # Add comments for each need
    for need in needs:
        need.comment_list = Comment.objects.filter(to_need=need)

    # Get project-level comments
    comments = Comment.objects.filter(to_project=content)

    context = {
        "content": content,
        "needs": needs,
        "tasks": content.task_set.all(),  # Assuming a reverse relation from Project to Task
        "comments": comments,
    }
    return render(request, "details.html", context=context)

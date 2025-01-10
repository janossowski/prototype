from django.urls import path
from . import views

app_name = "task"

urlpatterns = [
    path("<int:task_id>/", views.task_detail, name="task_detail"),
]

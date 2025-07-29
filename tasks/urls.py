from django.urls import path

from tasks.views import (
    index, TaskListView,
    WorkerListView,
    WorkerDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    TeamListView,
    TeamDetailView,
)

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),
    path("dashboard/", TaskListView.as_view(), name="task-list"),
    path("dashboard/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("dashboard/create/", TaskCreateView.as_view(), name="task-create"),
    path("dashboard/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("dashboard/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("members/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]
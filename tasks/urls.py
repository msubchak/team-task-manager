from django.urls import path

from tasks.views import (
    index, TaskListView,
    WorkerListView,
    WorkerDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
)

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),
    path("dashboard/", TaskListView.as_view(), name="task-list"),
    path("dashboard/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("dashboard/create/", TaskCreateView.as_view(), name="task-create"),
    path("dashboard/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("dashboard/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]
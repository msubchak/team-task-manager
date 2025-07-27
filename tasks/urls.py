from django.urls import path

from tasks.views import index, TaskListView, WorkerListView, WorkerDetailView

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),
    path("dashboard/", TaskListView.as_view(), name="task-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]
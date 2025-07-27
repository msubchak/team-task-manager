from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from tasks.models import Worker, Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    context = {
        "num_worker": num_worker,
    }
    return render(request, "tasks/index.html", context=context)


class TaskListView(ListView):
    model = Task


class WorkerListView(ListView):
    model = Worker


class WorkerDetailView(DetailView):
    model = Worker

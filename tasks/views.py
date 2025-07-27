from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from tasks.models import Worker, Task


#@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    context = {
        "num_worker": num_worker,
    }
    return render(request, "tasks/index.html", context=context)


class TaskListView(ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_in_progress"] = Task.objects.filter(is_complete=False).count()
        context["num_done"] = Task.objects.filter(is_complete=True).count()
        return context


class TaskCreateView(CreateView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")
    fields = "__all__"


class TaskDetailView(DetailView):
    model = Task


class TaskUpdateView(UpdateView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")
    fields = "__all__"


class WorkerListView(ListView):
    model = Worker


class WorkerDetailView(DetailView):
    model = Worker

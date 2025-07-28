from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.models import Worker, Task


login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    context = {
        "num_worker": num_worker,
    }
    return render(request, "tasks/index.html", context=context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_in_progress"] = Task.objects.filter(is_complete=False).count()
        context["num_done"] = Task.objects.filter(is_complete=True).count()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    fields = "__all__"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/task_delete.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    fields = "__all__"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker

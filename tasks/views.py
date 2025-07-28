from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.forms import TaskForm, WorkerTaskSearchForm, WorkerSearchForm
from tasks.models import Worker, Task


login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    tasks = Task.objects.all().order_by('-id')[:5]
    context = {
        "num_worker": num_worker,
        "tasks": tasks,
    }
    return render(request, "tasks/index.html", context=context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_in_progress"] = Task.objects.filter(is_complete=False).count()
        context["num_done"] = Task.objects.filter(is_complete=True).count()
        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerTaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
        form = WorkerTaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/task_delete.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    form_class = TaskForm


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get(
            "username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerTaskSearchForm(
            initial={"name": name}
        )
        tasks = worker.task_set.all()
        if name:
            tasks = tasks.filter(name__icontains=name)
        context["tasks"] = tasks
        return context

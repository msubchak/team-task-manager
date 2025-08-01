from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import context
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.forms import TaskForm, WorkerTaskSearchForm, WorkerSearchForm, WorkerCreateForm, ProjectCreateForm, \
    ProjectSearchForm, WorkerUpdateForm
from tasks.models import Worker, Task, Project, Team


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    tasks = Task.objects.all().order_by('-id')[:5]
    projects = Project.objects.all().order_by('-id')[:3]
    context = {
        "num_worker": num_worker,
        "tasks": tasks,
        "projects": projects,
    }
    return render(request, "tasks/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_in_progress"] = Task.objects.filter(is_complete=False).count()
        context["num_done"] = Task.objects.filter(is_complete=True).count()
        context["num_projects"] = Project.objects.count()
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


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/task_delete.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    form_class = TaskForm


class WorkerListView(LoginRequiredMixin, generic.ListView):
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


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
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

    def get_queryset(self):
        return Worker.objects.annotate(
            complete_tasks=Count(
                "task",
                filter=Q(task__is_complete=True),
                distinct=True
            ),
            in_progress_tasks=Count(
                "task",
                filter=Q(task__is_complete=False),
                distinct=True
            )
        )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("tasks:worker-list")
    template_name = "tasks/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("tasks:worker-list")
    template_name = "tasks/worker_form.html"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")
    template_name = "tasks/worker_delete.html"


class WorkerTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/worker_tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(WorkerTaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerTaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        worker_id = self.kwargs["pk"]
        queryset = Task.objects.filter(assignees=worker_id).distinct()
        form = WorkerTaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team

    def get_queryset(self):
        return Team.objects.annotate(
            num_workers=Count("workers", distinct=True),
            num_projects=Count("project", distinct=True),
            num_tasks=Count("workers__task", distinct=True),
            complete_tasks=Count(
                "workers__task",
                filter=Q(workers__task__is_complete=True),
                distinct=True
            ),
            in_progress_tasks=Count(
                "workers__task",
                filter=Q(workers__task__is_complete=False),
                distinct=True
            )
        )


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workers"] = self.object.workers.all()
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("tasks:team-list")
    template_name = "tasks/team_form.html"


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("tasks:team-list")
    template_name = "tasks/team_form.html"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")
    template_name = "tasks/team_delete.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return Project.objects.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("tasks:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("tasks:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:project-list")
    template_name = "tasks/project_delete.html"


class ProjectTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/project_tasks.html"
    context_object_name = "tasks"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(ProjectTaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerTaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        worker_id = self.kwargs["pk"]
        queryset = Task.objects.filter(project_id=worker_id).distinct()
        form = WorkerTaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

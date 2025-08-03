from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Position, TaskType, Project, Task


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password1!"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(
            name = "test"
        )
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="pass3123!",
            position=position,
            email="expample@example.com"
        )

    def test_worker_position_listed(self):
        url = reverse("admin:tasks_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position.name)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:tasks_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position.name)

    def test_worker_create_position_listed(self):
        url = reverse("admin:tasks_worker_add")
        response = self.client.get(url)
        self.assertContains(response, 'name="position"')


class TaskAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password1!"
        )
        self.client.force_login(self.admin_user)
        self.task_type = TaskType.objects.create(name="test")
        self.project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=self.task_type,
            project=self.project
        )

    def test_task_list_display(self):
        url = reverse("admin:tasks_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Name")
        self.assertContains(response, "Deadline")
        self.assertContains(response, "Is complete")
        self.assertContains(response, "Priority")
        self.assertContains(response, "Task type")
        self.assertContains(response, "Project")

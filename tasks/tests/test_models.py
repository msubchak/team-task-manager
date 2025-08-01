from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.models import (
    TaskType,
    Tag,
    Project,
    Position,
    Team,
    Worker, Task
)


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task = TaskType.objects.create(name="test")
        self.assertEqual(str(task), "test")

    def test_tag_str(self):
        tag = Tag.objects.create(name="test")
        self.assertEqual(str(tag), "test")

    def test_project_str(self):
        project = Project.objects.create(name="test")
        self.assertEqual(str(project), "test")

    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), "test")

    def test_team_str(self):
        team = Team.objects.create(name="test")
        self.assertEqual(str(team), "test")

    def test_create_worker_with_position(self):
        username="test1234"
        password="test1234!"
        position=Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(password))

    def test_create_worker_with_team(self):
        username = "test1234"
        password = "test1234!"
        team = Team.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            team=team,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.team, team)
        self.assertTrue(worker.check_password(password))

    def test_create_task_with_priority(self):
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(
            name="test",
            description="test",
        )
        urgent = Task.Priority.URGENT
        task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project,
            priority=urgent,
        )
        self.assertEqual(task.priority, urgent)
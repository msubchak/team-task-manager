from django.test import TestCase

from tasks.models import (
    TaskType,
    Tag,
    Project,
    Position,
    Team,
    Worker
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
        worker = Worker.objects.create(
            username=username,
            password=password,
            position=position,
        )


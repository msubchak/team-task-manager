from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, TaskType, Project, Worker, Position, Team


class PublicIndexViewTest(TestCase):
    def setUp(self):
        self.urls = reverse("tasks:index")

    def test_login_required_index(self):
        response = self.client.get(self.urls)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123412!",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertIn("num_worker", response.context)
        self.assertIn("tasks", response.context)
        self.assertIn("projects", response.context)


class PublicTaskListTest(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.urls = {
            "list": reverse("tasks:task-list"),
            "create": reverse("tasks:task-create"),
            "detail": reverse("tasks:task-detail", args=[self.task.id]),
            "update": reverse("tasks:task-update", args=[self.task.id]),
            "delete": reverse("tasks:task-delete", args=[self.task.id]),
        }

    def test_login_required_list(self):
        response = self.client.get(self.urls["list"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self):
        response = self.client.get(self.urls["create"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_detail(self):
        response = self.client.get(self.urls["detail"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_update(self):
        response = self.client.get(self.urls["update"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_delete(self):
        response = self.client.get(self.urls["delete"])
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123412!",
        )
        self.client.force_login(self.user)
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.url = reverse("tasks:task-list")

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_context_task_num_workers(self):
        response = self.client.get(self.url)
        self.assertIn("num_workers", response.context)

    def test_context_task_num_tasks(self):
        response = self.client.get(self.url)
        self.assertIn("num_tasks", response.context)

    def test_context_task_num_in_progress(self):
        response = self.client.get(self.url)
        self.assertIn("num_in_progress", response.context)

    def test_context_task_num_done(self):
        response = self.client.get(self.url)
        self.assertIn("num_done", response.context)

    def test_context_task_num_projects(self):
        response = self.client.get(self.url)
        self.assertIn("num_projects", response.context)

    def test_task_in_task_list(self):
        response = self.client.get(self.url)
        self.assertIn(self.task, response.context["task_list"])

    def test_queryset_filter_by_name(self):
        response = self.client.get(self.url, {"name": "test"})
        self.assertEqual(response.status_code, 200)
        for task in response.context["task_list"]:
            self.assertIn("test", task.name)


class PublicWorkerListTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="QA")
        team = Team.objects.create(name="team")
        self.worker = Worker.objects.create(
            position=position,
            team=team,
        )
        self.urls = {
            "list": reverse("tasks:worker-list"),
            "create": reverse("tasks:worker-create"),
            "detail": reverse("tasks:worker-detail", args=[self.worker.id]),
            "update": reverse("tasks:worker-update", args=[self.worker.id]),
            "delete": reverse("tasks:worker-delete", args=[self.worker.id]),
        }

    def test_login_required_list(self):
        response = self.client.get(self.urls["list"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self):
        response = self.client.get(self.urls["create"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_detail(self):
        response = self.client.get(self.urls["detail"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_update(self):
        response = self.client.get(self.urls["update"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_delete(self):
        response = self.client.get(self.urls["delete"])
        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerListTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="QA")
        team = Team.objects.create(name="team")
        self.worker_one = Worker.objects.create(
            username="worker1",
            email="worker1@example.com",
            position=position,
            team=team,
        )
        self.worker_two = Worker.objects.create(
            username="worker2",
            email="worker2@example.com",
            position=position,
            team=team,
        )
        self.url = reverse("tasks:worker-list")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123412!",
        )
        self.client.force_login(self.user)

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_list.html")

    def test_worker_list_in_context(self):
        response = self.client.get(self.url)
        worker_list = Worker.objects.all()
        self.assertEqual(list(response.context["worker_list"]), list(worker_list))

    def test_num_workers_in_context(self):
        response = self.client.get(self.url)
        self.assertIn("num_workers", response.context)

    def test_num_workers_value(self):
        response = self.client.get(self.url)
        worker_list = Worker.objects.all()
        self.assertEqual(response.context["num_workers"], worker_list.count())

    def test_queryset_filter_by_username(self):
        response = self.client.get(self.url, {"username": "worker"})
        self.assertEqual(response.status_code, 200)
        for worker in response.context["worker_list"]:
            self.assertIn("worker", worker.username)


class PublicWorkerTaskListTest(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        worker = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.urls = reverse("tasks:worker-tasks", args=[worker.id])

    def test_login_required_worker_tasks(self):
        response = self.client.get(self.urls)
        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerTaskListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123412!",
        )
        self.client.force_login(self.user)
        position = Position.objects.create(name="QA")
        team = Team.objects.create(name="team")
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.worker = Worker.objects.create(
            username="worker1",
            position=position,
            team=team,
            email="test@gmail.com"
        )
        self.task.assignees.add(self.worker)
        self.url = reverse("tasks:worker-tasks", args=[self.worker.id])

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_tasks.html")

    def test_queryset_filter_by_username(self):
        response = self.client.get(self.url, {"name": "test"})
        self.assertEqual(response.status_code, 200)
        for task in response.context["tasks"]:
            self.assertIn("test", task.name)


class PublicTeamListTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="team")
        self.urls = {
            "list": reverse("tasks:team-list"),
            "create": reverse("tasks:team-create"),
            "detail": reverse("tasks:team-detail", args=[self.team.id]),
            "update": reverse("tasks:team-update", args=[self.team.id]),
            "delete": reverse("tasks:team-delete", args=[self.team.id]),
        }

    def test_login_required_list(self):
        response = self.client.get(self.urls["list"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self):
        response = self.client.get(self.urls["create"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_detail(self):
        response = self.client.get(self.urls["detail"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_update(self):
        response = self.client.get(self.urls["update"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_delete(self):
        response = self.client.get(self.urls["delete"])
        self.assertNotEqual(response.status_code, 200)


class PrivateTeamListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234!"
        )
        self.client.force_login(self.user)

        Team.objects.create(name="test1")
        Team.objects.create(name="test")
        self.url = reverse("tasks:team-list")

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/team_list.html")

    def test_team_list_in_context(self):
        response = self.client.get(self.url)
        team_list = Team.objects.all()
        self.assertEqual(list(response.context["team_list"]), list(team_list))


class PrivateTeamDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234!"
        )
        self.client.force_login(self.user)
        team = Team.objects.create(name="test1")
        position = Position.objects.create(name="QA")
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.worker = Worker.objects.create(
            username="worker1",
            team=team,
            position=position,
            email="email@gmail.com"
        )
        self.url = reverse("tasks:team-detail", args=[team.id])

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/team_detail.html")

    def test_context_team_workers(self):
        response = self.client.get(self.url)
        self.assertIn("workers", response.context)

    def test_context_team_num_workers(self):
        response = self.client.get(self.url)
        self.assertIn("num_workers", response.context)

    def test_context_team_num_projects(self):
        response = self.client.get(self.url)
        self.assertIn("num_projects", response.context)

    def test_context_team_complete_tasks(self):
        response = self.client.get(self.url)
        self.assertIn("complete_tasks", response.context)

    def test_context_team_in_progress(self):
        response = self.client.get(self.url)
        self.assertIn("in_progress", response.context)

    def test_context_team_assigned_tasks(self):
        response = self.client.get(self.url)
        self.assertIn("assigned_tasks", response.context)

    def test_context_team_num_tasks(self):
        response = self.client.get(self.url)
        self.assertIn("num_tasks", response.context)


class PublicProjectListTest(TestCase):
    def setUp(self):
        team = Team.objects.create(name="team")
        self.project = Project.objects.create(
            name="test",
            description="test",
        )
        self.project.team.set([team])
        self.urls = {
            "list": reverse("tasks:project-list"),
            "create": reverse("tasks:project-create"),
            "detail": reverse("tasks:project-detail", args=[self.project.id]),
            "update": reverse("tasks:project-update", args=[self.project.id]),
            "delete": reverse("tasks:project-delete", args=[self.project.id]),
        }

    def test_login_required_list(self):
        response = self.client.get(self.urls["list"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self):
        response = self.client.get(self.urls["create"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_detail(self):
        response = self.client.get(self.urls["detail"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_update(self):
        response = self.client.get(self.urls["update"])
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_delete(self):
        response = self.client.get(self.urls["delete"])
        self.assertNotEqual(response.status_code, 200)


class PrivateProjectListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1231"
        )
        self.client.force_login(self.user)
        team = Team.objects.create(name="team")
        project1 = Project.objects.create(
            name="test1",
            description="test1",
        )
        project1.team.set([team])
        project2 = Project.objects.create(
            name="test2",
            description="test2",
        )
        project2.team.set([team])
        self.url = reverse("tasks:project-list")

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/project_list.html")

    def test_project_list_in_context(self):
        response = self.client.get(self.url)
        project_list = Project.objects.all()
        self.assertEqual(list(response.context["project_list"]), list(project_list))

    def test_queryset_filter_by_name(self):
        response = self.client.get(self.url, {"name": "test"})
        self.assertEqual(response.status_code, 200)
        for project in response.context["project_list"]:
            self.assertIn("test", project.name)


class PublicProjectTaskListView(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.urls = reverse("tasks:project-tasks", args=[project.id])

    def test_login_required_project_tasks(self):
        response = self.client.get(self.urls)
        self.assertNotEqual(response.status_code, 200)


class PrivateProjectTaskListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123213!"
        )
        self.client.force_login(self.user)
        team = Team.objects.create(name="team")
        project = Project.objects.create(
            name="test",
            description="test",
        )
        project.team.set([team])
        task_type = TaskType.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.url = reverse("tasks:project-tasks", args=[project.id])

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/project_tasks.html")

    def test_queryset_filter_by_name(self):
        response = self.client.get(self.url, {"name": "test"})
        self.assertEqual(response.status_code, 200)
        for task in response.context["tasks"]:
            self.assertIn("test", task.name)

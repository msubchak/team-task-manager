from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.forms import WorkerTaskSearchForm
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
        self.url = reverse("tasks:index")

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_context_index_num_worker(self):
        response = self.client.get(self.url)
        self.assertIn("num_worker", response.context)

    def test_context_index_tasks(self):
        response = self.client.get(self.url)
        self.assertIn("tasks", response.context)

    def test_context_index_projects(self):
        response = self.client.get(self.url)
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


class PrivateTaskDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12312!"
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
        self.url = reverse("tasks:task-detail", args=[self.task.id])

    def test_task_detail_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_detail_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_detail.html")

    def test_task_detail_context_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["task"], self.task)


class PrivateTaskCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test3123"
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:task-create")

    def test_task_create_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_form.html")


class PrivateTaskUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test312312"
        )
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:task-update", args=[self.task.id])

    def test_task_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_form.html")


class PrivateTaskDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12312"
        )
        task_type = TaskType.objects.create(name="test")
        project = Project.objects.create(name="test")
        self.task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.now(),
            task_type=task_type,
            project=project
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:task-delete", args=[self.task.id])

    def test_task_delete_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_delete.html")


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


class PrivateWorkerDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123"
        )
        self.client.force_login(self.user)
        position = Position.objects.create(name="Dev")
        team = Team.objects.create(name="Team A")
        task_type = TaskType.objects.create(name="Bug")
        project = Project.objects.create(name="Project X")

        self.worker = Worker.objects.create(
            username="worker1",
            email="worker1@example.com",
            position=position,
            team=team,
        )
        self.task1 = Task.objects.create(
            name="Fix bug",
            description="Fix critical bug",
            deadline=datetime.now(),
            task_type=task_type,
            project=project,
        )
        self.task2 = Task.objects.create(
            name="Write tests",
            description="Write unit tests",
            deadline=datetime.now(),
            task_type=task_type,
            project=project,
            is_complete=True,
        )
        self.task1.assignees.add(self.worker)
        self.task2.assignees.add(self.worker)
        self.url = reverse("tasks:worker-detail", args=[self.worker.id])

    def test_worker_detail_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_worker_detail_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")

    def test_worker_detail_context_worker_search(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["worker"], self.worker)
        self.assertIsInstance(response.context["search_form"], WorkerTaskSearchForm)

    def test_worker_detail_in_context(self):
        response = self.client.get(self.url)
        tasks = response.context["tasks"]
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_worker_detail_filter_by_name(self):
        response = self.client.get(self.url, {"name": "test"})
        tasks = response.context["tasks"]
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task1, tasks)


class PrivateWorkerCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test3123"
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:worker-create")

    def test_worker_create_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_worker_create_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_form.html")


class PrivateWorkerUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test312312"
        )
        self.client.force_login(self.user)
        position = Position.objects.create(name="Dev")
        team = Team.objects.create(name="Team A")
        self.worker = Worker.objects.create(
            position=position,
            team=team,
            email="dsadd@gmail.com"
        )
        self.url = reverse("tasks:worker-update", args=[self.worker.id])

    def test_worker_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_worker_update_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_form.html")


class PrivateWorkerDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12312"
        )
        self.client.force_login(self.user)
        position = Position.objects.create(name="Dev")
        team = Team.objects.create(name="Team A")
        self.worker = Worker.objects.create(
            position=position,
            team=team,
            email="dsadd@gmail.com"
        )
        self.url = reverse("tasks:worker-delete", args=[self.worker.id])

    def test_worker_delete_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_worker_delete_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/worker_delete.html")


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


class PrivateTeamCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test3123"
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:team-create")

    def test_team_create_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_team_create_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/team_form.html")


class PrivateTeamUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test312312"
        )
        self.client.force_login(self.user)
        self.team = Team.objects.create(name="Team A")
        self.url = reverse("tasks:team-update", args=[self.team.id])

    def test_team_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_team_update_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/team_form.html")


class PrivateTeamDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12312"
        )
        self.client.force_login(self.user)
        self.team = Team.objects.create(name="Team A")
        self.url = reverse("tasks:team-delete", args=[self.team.id])

    def test_team_delete_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_team_delete_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/team_delete.html")


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


class PrivateProjectCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test3123"
        )
        self.client.force_login(self.user)
        self.url = reverse("tasks:project-create")

    def test_project_create_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_project_create_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/project_form.html")


class PrivateProjectUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test312312"
        )
        self.client.force_login(self.user)
        self.project = Project.objects.create(name="test")
        self.url = reverse("tasks:project-update", args=[self.project.id])

    def test_project_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_project_update_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/project_form.html")


class PrivateProjectDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12312"
        )
        self.client.force_login(self.user)
        self.project = Project.objects.create(name="test")
        self.url = reverse("tasks:project-delete", args=[self.project.id])

    def test_project_delete_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_project_delete_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/project_delete.html")


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

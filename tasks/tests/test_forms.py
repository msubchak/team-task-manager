from django.test import TestCase

from tasks.forms import WorkerCreateForm, WorkerUpdateForm, WorkerTaskSearchForm, WorkerSearchForm, ProjectCreateForm, \
    ProjectSearchForm, ProjectTaskSearchForm
from tasks.models import Position, Team


class BaseWorkerFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test")
        self.team = Team.objects.create(name="test")
        self.form_data = {
            "username": "test_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "test",
            "last_name": "lastname",
            "email": "example@gmail.com",
            "position": self.position.id,
            "team": self.team.id,
        }


class WorkerCreateFormTest(BaseWorkerFormTest):
    def test_worker_form_is_valid(self):
        form = WorkerCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["first_name"], self.form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], self.form_data["last_name"])
        self.assertEqual(form.cleaned_data["username"], self.form_data["username"])
        self.assertEqual(form.cleaned_data["email"], self.form_data["email"])
        self.assertEqual(form.cleaned_data["position"], self.position)
        self.assertEqual(form.cleaned_data["team"], self.team)


class WorkerUpdateFormTest(BaseWorkerFormTest):
    def test_worker_form_is_valid(self):
        form = WorkerUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["first_name"], self.form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], self.form_data["last_name"])
        self.assertEqual(form.cleaned_data["username"], self.form_data["username"])
        self.assertEqual(form.cleaned_data["email"], self.form_data["email"])
        self.assertEqual(form.cleaned_data["position"], self.position)
        self.assertEqual(form.cleaned_data["team"], self.team)


class WorkerTaskSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {"name": "task"}
        form = WorkerTaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "task")

    def test_search_valid_empty_name(self):
        form_data = {"name": ""}
        form = WorkerTaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_search_with_long_name(self):
        form_data = {"name": "a" * 300}
        form = WorkerTaskSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class WorkerSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_search_valid_empty_username(self):
        form_data = {"username": ""}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_search_with_long_name(self):
        form_data = {"username": "a" * 300}
        form = WorkerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ProjectCreateFormTest(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name="test1")
        self.team2 = Team.objects.create(name="test2")

    def test_form_valida_data(self):
        form_data = {
            "name": "test1",
            "description": "test",
            "team": [self.team1.id, self.team2.id],
        }
        form = ProjectCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test1")
        self.assertEqual(form.cleaned_data["description"], "test")
        self.assertEqual(list(form.cleaned_data["team"]), list([self.team1, self.team2]))


class ProjectSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {"name": "test"}
        form = ProjectSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test")

    def test_search_valid_empty_project_name(self):
        form_data = {"name": ""}
        form = ProjectSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_search_with_long_name(self):
        form_data = {"name": "a" * 300}
        form = ProjectSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class ProjectTaskSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {"name": "test"}
        form = ProjectTaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test")

    def test_search_valid_empty_project_name(self):
        form_data = {"name": ""}
        form = ProjectTaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_search_with_long_name(self):
        form_data = {"name": "a" * 300}
        form = ProjectTaskSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

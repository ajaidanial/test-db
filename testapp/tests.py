# content of test_sample.py
import pytest

from testapp import views, models

pytestmark = pytest.mark.django_db


def test_get_user(create_test_user):
    assert views.get_user('test_user').name == 'test_user'


def test_tasks_created_by_user(create_test_data_1):
    result = views.tasks_created_by_user('test_user')
    test = models.Task.objects.get(name='test_task_1')
    assert len(result) == 1
    assert result[0] == test


def test_has_user_open_tasks(create_test_data_1):
    assert views.has_user_open_tasks('test_user') == True


def test_clear_all_tasks_for_user():
    pass


def test_tasks_with_expired_due_date(create_test_data_1):
    tasks = views.tasks_with_expired_due_date('test_user')
    assert len(tasks) == 1
    assert tasks[0] == models.Task.objects.get(name="test_task_1")


def test_tasks_with_three_days_due(create_test_data_2):
    tasks = views.tasks_with_three_days_due('test_user')
    assert len(tasks) == 1
    assert tasks[0] == models.Task.objects.get(name="test_task_1")

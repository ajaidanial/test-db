# content of test_sample.py
import pytest

from testapp import views, models

pytestmark = pytest.mark.django_db


def test_get_user(get_user):
    assert views.get_user('test_user').name == 'test_user'


def test_tasks_created_by_user(tasks_created_by_user):
    result = views.tasks_created_by_user('test_user')
    test = models.Task.objects.get(name='test_task_1')
    assert len(result) == 1
    assert result[0] == test

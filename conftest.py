from datetime import datetime

import pytest

from testapp import models


@pytest.fixture
def create_test_user():
    user = models.User(name='test_user')
    user.save()


@pytest.fixture
def create_test_data_1():
    user = models.User(name='test_user')
    user.save()
    task_list = models.TaskList(
        name='test_task_list',
        desc="test_desc",
        created_date=datetime.now().date(),
        creator=user,
    )
    task_list.save()
    task = models.Task(
        name='test_task_1',
        description="test_desc",
        created_date=datetime.now().date(),
        due_date=datetime(2019, 5, 7),
        creator=user,
        task_list=task_list,
        is_open=True,
    )
    task.save()
    task.assigned_users.add(user)


@pytest.fixture
def create_test_data_2():
    today = datetime.now().date()
    three_days_ahead = datetime(today.year, today.month, today.day + 3)
    user = models.User(name='test_user')
    user.save()
    task_list = models.TaskList(
        name='test_task_list',
        desc="test_desc",
        created_date=datetime.now().date(),
        creator=user,
    )
    task_list.save()
    task = models.Task(
        name='test_task_1',
        description="test_desc",
        created_date=today,
        due_date=three_days_ahead,
        creator=user,
        task_list=task_list,
        is_open=True,
    )
    task.save()
    task.assigned_users.add(user)

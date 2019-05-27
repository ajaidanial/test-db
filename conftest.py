from datetime import datetime

import pytest

from testapp import models


@pytest.fixture
def get_user():
    user = models.User(name='test_user')
    user.save()


@pytest.fixture
def tasks_created_by_user():
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
        due_date=datetime.now().date(),
        creator=user,
        task_list=task_list,
    )
    task.save()

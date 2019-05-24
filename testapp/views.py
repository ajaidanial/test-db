from typing import List

from testapp.models import *


def clear_all_tasks_for_user(name: str) -> None:
    user = User.objects.get(name=name)
    for task in user.assigned_tasks.all():
        task.is_open = False
        task.save()


def has_user_open_tasks(name: str) -> List[str]:
    user = User.objects.get(name=name)
    open_tasks = []
    for task in user.assigned_tasks.all():
        if task.is_open:
            open_tasks.append(task.name)
    return open_tasks


def tasks_created_by_user(name: str) -> List[str]:
    user = User.objects.get(name=name)
    created_tasks = []
    for task in user.assigned_tasks.all():
        if task.creator.name == user.name:
            created_tasks.append(user.name)
    return created_tasks

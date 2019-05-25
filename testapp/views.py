from datetime import datetime
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
    for task in user.created_tasks.all():
        # if task.creator.name == user.name:
        created_tasks.append(task.name)
    return created_tasks


def tasks_with_expired_due_date(name: str) -> List[str]:
    user = User.objects.get(name=name)
    due_tasks = []
    for task in user.assigned_tasks.all():
        if task.due_date > datetime.now().date():
            due_tasks.append(task.name)
    return due_tasks


def tasks_with_three_days_due(name: str) -> List[str]:
    user = User.objects.get(name=name)
    due_tasks: List[str] = []
    for task in user.assigned_tasks.all():
        if 3 >= (datetime.now().date() - task.due_date).days > 0:
            due_tasks.append(task.name)
    return due_tasks


def task_desc(name: str) -> List[str]:
    user = User.objects.prefetch_related('assigned_tasks__task_list').get(name=name)
    for task in user.assigned_tasks.all():
        print("Task Name: ", task.name)
        print("Task desc: ", task.description)
        print("Task due date: ", task.due_date)
        print("Task List: ", task.task_list)
        print("------------------------------------")

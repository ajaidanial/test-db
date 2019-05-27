from datetime import datetime

from django.db.models.query import QuerySet

from testapp.models import *


def clear_all_tasks_for_user(name: str) -> None:
    user = get_user(name, prefetch="assigned_tasks")
    user.assigned_tasks.update(is_open=False)


def has_user_open_tasks(name: str) -> bool:
    if Task.objects.filter(is_open=True, assigned_users=get_user(name)).count():
        return True
    return False


def tasks_created_by_user(name: str) -> QuerySet:
    return Task.objects.filter(creator=get_user(name))


def tasks_with_expired_due_date(name: str) -> QuerySet:
    return Task.objects.filter(due_date__lt=datetime.now().date(), assigned_users=get_user(name))


def tasks_with_three_days_due(name: str) -> QuerySet:
    today = datetime.now().date()
    three_days_ahead = datetime(today.year, today.month, today.day + 3)
    print(three_days_ahead.date())
    return Task.objects.filter(due_date__gt=today, assigned_users=get_user(name), due_date__lte=three_days_ahead)


def tasks_desc_for_user(name: str) -> None:
    tasks = Task.objects.prefetch_related('assigned_users').filter(assigned_users=get_user(name))
    display_task_data_for_user(tasks)


def get_user(name, prefetch="") -> User:
    try:
        return User.objects.prefetch_related(prefetch).get(name=name)
    except AttributeError:
        return User.objects.get(name=name)


def display_task_data_for_user(tasks: dict) -> None:
    for t in tasks:
        print(t)
        print("---------------------------------")

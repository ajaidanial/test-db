from datetime import datetime

from django.db.models.query import QuerySet
from rest_framework.authtoken.models import Token

from testapp.models import *
from testapp.serializers import UserSerializer


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
    tasks = Task.objects.prefetch_related('assigned_users').filter(assigned_users=get_user(name)).values()
    display_task_data_for_user(tasks)


def get_user(name, prefetch="") -> User:
    if prefetch != "":
        return User.objects.prefetch_related(prefetch).get(username=name)
    else:
        return User.objects.get(username=name)


def display_task_data_for_user(tasks: dict) -> None:
    for task in tasks:
        print(task)


def create_user(name: str, email: str) -> None:
    user: User = User(name=name, email=email)
    user.save()
    return user.key


def return_user_dict(user: User) -> dict:
    token = Token.objects.get(user=user)
    data: dict = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'token': token.key
    }
    return data


# TODO: look here

# For api request


def login_or_singup_user_and_return_token(username: str, password: str, email: str = None) -> dict:
    if email is None:  # login of user
        return return_user_dict(get_user(username))  # TODO: username and password check | does not exist
    else:  # sign up for user
        data: dict = {'username': username, 'password': password, 'email': email}
        user = UserSerializer(data=data)
        if user.is_valid():
            user.save()
            token = Token.objects.create(user=get_user(username))
            return_data = user.data
            return_data['token'] = token.key
            return return_data
        else:
            return user.errors

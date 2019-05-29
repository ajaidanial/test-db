from datetime import datetime
from itertools import chain
from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
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


def create_tasklist_api(username: str, received_token: str, tasklist_name: str) -> dict:
    user = get_user(username)
    if is_authenticated_user(user, received_token):
        try:
            tasklist = TaskList(name=tasklist_name, creator=user, created_date=datetime.now().date())
            tasklist.save()
        except IntegrityError:
            return {"message": "Tasklist already present"}
        return {
            'tasklist_name': tasklist_name,
            'craetor': username,
            'created_date': datetime.now().date(),
            'tasklist_id': tasklist.pk,
        }
    else:
        return {"message": "User not authenticated"}


def delete_tasklist_api(username: str, received_token: str, tasklist_name: str) -> dict:
    user = get_user(username)
    if is_authenticated_user(user, received_token):
        try:
            tasklist = TaskList.objects.get(name=tasklist_name, creator=user)
            tasklist.delete()
        except ObjectDoesNotExist:
            return {"message": "Tasklist not present"}
        return {'success': True, }
    else:
        return {"message": "User not authenticated"}


def is_authenticated_user(user: User, received_token: str):
    if Token.objects.get(user=user).key == received_token:
        return True
    return False


def get_tasks_for_user(username: str, received_token: str) -> dict:
    user = get_user(username, prefetch='assigned_tasks')
    if is_authenticated_user(user, received_token):
        assigned_task_names = list(task.name for task in user.assigned_tasks.all())
        return_data = {'username': user.username, 'assigned_tasks': assigned_task_names}
        return return_data
    else:
        return {"message": "User not authenticated"}


def close_task(taskname: str, username: str, received_token: str) -> dict:
    user = get_user(username)
    if is_authenticated_user(user, received_token):
        try:
            task = Task.objects.get(name=taskname)
            task.is_open = False
            task.save()
            return {"message": "Task closed"}
        except ObjectDoesNotExist:
            return {"message": "Task does not exists"}
    else:
        return {"message": "User not authenticated"}


def delete_task(taskname: str, username: str, received_token: str) -> dict:
    user = get_user(username)
    if is_authenticated_user(user, received_token):
        try:
            Task.objects.get(name=taskname, creator=user).delete()
            return {"message": "Task deleted"}
        except ObjectDoesNotExist:
            return {"message": "Task does not exists || Permission error"}
    else:
        return {"message": "User not authenticated"}


def create_task(
        taskname: str,
        due_date: datetime.now().date(),
        is_open: bool,
        assigned_users: list,
        tasklist: str,
        username: str,
        received_token: str,
):
    user = get_user(username)
    if is_authenticated_user(user, received_token):
        try:
            try:
                user_list = [User.objects.get(username=assigned_users_name) for assigned_users_name in
                             assigned_users.split(',')]
            except ObjectDoesNotExist:
                return {"message": "User does not exists | aborted action"}
            task = Task.objects.create(
                name=taskname,
                created_date=datetime.now().date(),
                due_date=due_date,
                is_open=is_open,
                creator=user,
                task_list=TaskList.objects.get(name=tasklist),
            )
            for user in user_list:
                task.assigned_users.add(user)
            task.save()
            return {"message": "Task created"}
        except IntegrityError:
            return {"message": "Task already exists"}
    else:
        return {"message": "User not authenticated"}


def get_all_tasks(received_token: str) -> Dict[str, dict]:  # returns all the tasks
    if is_user_authenticated_by_token(received_token):
        tasks = Task.objects.prefetch_related("assigned_users").all()
        return_dict = {}
        for task in tasks:
            return_dict[task.name] = instance2dict(task)
        return return_dict
    else:
        return {"response": {'success': False, "message": "Token invalid"}}


def instance2dict(instance):  # helper function to get many to many relations
    from django.db.models.fields.related import ManyToManyField
    metas = instance._meta
    data = {}
    for f in chain(metas.concrete_fields, metas.many_to_many):
        if isinstance(f, ManyToManyField):
            data[str(f.name)] = [tmp_object.username
                                 for tmp_object in f.value_from_object(instance)]
        else:
            data[str(f.name)] = str(getattr(instance, f.name, False))
    return data


def is_user_authenticated_by_token(received_token: str) -> bool:
    try:
        user = Token.objects.get(key=received_token).user
        return True
    except ObjectDoesNotExist:
        return False

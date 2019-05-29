from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from testapp import database_operations


@csrf_exempt
def user_op(request):
    if request.method == 'GET':
        try:
            username: str = request.GET['username']
            password: str = request.GET['password']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        return JsonResponse(database_operations.login_or_singup_user_and_return_token(username, password))
    if request.method == 'POST':
        try:
            username: str = request.POST['username']
            password: str = request.POST['password']
            email: str = request.POST['email']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        return JsonResponse(database_operations.login_or_singup_user_and_return_token(username, password, email))

    return HttpResponse(None)


@csrf_exempt
def task_op(request):
    if request.method == 'GET':
        received_token: str = request.META.get('HTTP_AUTHORIZATION')
        return JsonResponse(database_operations.get_all_tasks(received_token))
    if request.method == 'POST':
        try:
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
            data = json.loads(request.body)
            name: str = data['name']
            due_date: str = data['due_date']
            is_open: bool = data['is_open']
            assigned_users: str = data['assigned_users']
            task_list: str = data['task_list']

        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse(
                {'success': False, 'required data': 'name, due_date, is_open, assigned_users, task_list'})
        return JsonResponse(database_operations.create_task(
            taskname=name,
            due_date=due_date,
            is_open=is_open,
            assigned_users=assigned_users,
            tasklist=task_list,
            received_token=received_token,
        ))
        pass
    return HttpResponse(None)


"""
    if request.method == 'POST':  # to create, delete and close a task
        try:
            command: str = request.POST['command']
            username: str = request.POST['username']
            taskname: str = request.POST['task_name']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
        except MultiValueDictKeyError:
            return HttpResponse(None)
        if command == 'create':
            due_date: datetime.now().date() = request.POST['due_date']
            tasklist_name: str = request.POST['tasklist_name']
            is_open: bool = request.POST['is_open']
            assigned_users: list = request.POST['assigned_users']
            return JsonResponse(database_operations.create_task(
                taskname=taskname,
                due_date=due_date,
                is_open=is_open,
                assigned_users=assigned_users,
                tasklist=tasklist_name,
                username=username,
                received_token=received_token,
            ))
        if command == 'delete':
            return JsonResponse(database_operations.delete_task(taskname, username, received_token))
        if command == 'close':
            return JsonResponse(database_operations.close_task(taskname, username, received_token))
        return HttpResponse(None)

    if request.method == 'GET':  # to display assigned task to user
        try:
            username: str = request.GET['username']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
        except MultiValueDictKeyError:
            return HttpResponse(None)
        return JsonResponse(database_operations.get_tasks_for_user(username, received_token))
    return HttpResponse(None)
"""


@csrf_exempt
def tasklist_op(request):
    if request.method == 'POST':
        try:
            command: str = request.POST['command']
            username: str = request.POST['username']
            tasklist_name: str = request.POST['tasklist_name']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
        except MultiValueDictKeyError:
            return HttpResponse(None)
        if command == 'create':
            return JsonResponse(database_operations.create_tasklist_api(username, received_token, tasklist_name))
        if command == 'delete':
            return JsonResponse(database_operations.delete_tasklist_api(username, received_token, tasklist_name))
        return HttpResponse(None)
    return HttpResponse(None)


@csrf_exempt
def task_delete_update(request, id):
    received_token: str = request.META.get('HTTP_AUTHORIZATION')
    if request.method == "DELETE":
        return JsonResponse(database_operations.delete_task(id, received_token))
    if request.method == "PUT":
        received_token: str = request.META.get('HTTP_AUTHORIZATION')
        data = json.loads(request.body)
        if data == {}:
            return HttpResponse(None)
        return JsonResponse(database_operations.update_task(data, received_token))
    return HttpResponse(None)


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username: str = data['username']
            password: str = data['password']
            email: str = data['email']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse({'success': False, 'required data': 'username, password, email'})
        return JsonResponse(database_operations.singup_user_and_return_token(username, password, email))
    else:
        return HttpResponse(None)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username: str = data['username']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse({'success': False, 'required data': 'username'})
        return JsonResponse(database_operations.login_user(username, received_token))
    else:
        return HttpResponse(None)


"""
All POST data in JSON type
# /register: POST {username, email, password}
# /login: POST {username, password}
# /task: POST {...} create a task
# /task/<task_id>: DELETE deletes the task
# /tasks: GET - return all tasks with id and ...
/task/<task_id>: PUT {...} update tasks

Identifier: Token only
"""
# TODO: json format

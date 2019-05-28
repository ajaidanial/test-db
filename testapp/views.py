from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

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
    if request.method == 'POST':  # to create, delete and close a task
        try:
            command: str = request.POST['command']
            username: str = request.POST['username']
            taskname: str = request.POST['task_name']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
        except MultiValueDictKeyError:
            return HttpResponse(None)
        if command == 'create':
            due_date: str = request.POST['due_date']
            tasklist_name: str = request.POST['task_name']
            is_open: bool = request.POST['is_open']
            assigned_users: list = request.POST['assigned_users']
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


"""
# user op '/'
#     - login (token)
#     - register (tokeb)

# tasklist 'tasklist'
#     - create
#     - delete

task 'task'
    - delete
    - create
    - get all tasks for user
    - close task
"""

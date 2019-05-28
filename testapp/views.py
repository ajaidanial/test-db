from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from testapp import database_operations
from testapp.serializers import TaskListSerializer


@csrf_exempt
def user_op(request):
    try:
        username: str = request.GET['username']
        password: str = request.GET['password']
        if request.GET['email'] is not None:
            email: str = request.GET['email']
    except MultiValueDictKeyError:
        return None

    if request.method == 'GET':
        return database_operations.login_or_singup_user_and_return_token(username, password)
    if request.method == 'POST':
        database_operations.login_or_singup_user_and_return_token(username, password, email)
    return None


@csrf_exempt
def task_op(request):
    return HttpResponse("task op")


@csrf_exempt
def tasklist_op(request):
    if request.method == 'POST':
        tasklist = TaskListSerializer(data=dict(request.POST.items()))
        if tasklist.is_valid():
            tasklist.save()
            return JsonResponse(tasklist.data)
        #     TODO: token auth
        else:
            return JsonResponse(tasklist.errors)
    return HttpResponse("tasklist op")


"""
user op '/'
    - login (token)
    - register (tokeb)

tasklist 'tasklist'
    - create
    - delete

task 'task'
    - delete
    - create
    - get all tasks for user
    - close task
"""

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
    return HttpResponse("task op")


@csrf_exempt
def tasklist_op(request):
    if request.method == 'POST':
        try:
            username: str = request.POST['username']
            tasklist_name: str = request.POST['taslklist_name']
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
            # return HttpResponse(received_token)
        except MultiValueDictKeyError:
            return HttpResponse("hello")
        return JsonResponse(database_operations.create_tasklist_api(username, received_token, tasklist_name))
    if request.method == 'DELETE':
        pass
    return HttpResponse(None)


"""
# user op '/'
#     - login (token)
#     - register (tokeb)

tasklist 'tasklist'
    - create
    - delete

task 'task'
    - delete
    - create
    - get all tasks for user
    - close task
"""

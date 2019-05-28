from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from testapp.models import User
from testapp.serializers import UserSerializer, TaskListSerializer


@csrf_exempt
def user_op(request):
    if request.method == 'GET':
        try:
            name: str = request.GET['name']
            password: str = request.GET['password']
            return HttpResponse(name + " " + password)
        #     TODO: token auth
        except MultiValueDictKeyError:
            return HttpResponse(None)
    elif request.method == 'POST':
        user = UserSerializer(data=dict(request.POST.items()))
        if user.is_valid():
            user.save()
            u = User.objects.get(name=request.POST.get('name'))
            token = Token.objects.create(user=u)
            print(token)
            return JsonResponse(user.data)
        #     TODO: token auth
        else:
            return JsonResponse(user.errors)
    else:
        return HttpResponse("user op")


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

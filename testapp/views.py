from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from testapp.serializers import SnippetSerializer


@csrf_exempt
def user_op(request):
    if request.method == 'GET':
        name: str = request.GET['name']
        email: str = request.GET['email']
        return HttpResponse(name + " " + email)
    elif request.method == 'POST':
        user = SnippetSerializer(data=dict(request.POST.items()))
        if user.is_valid():
            user.save()
            return JsonResponse(user.data, status=201)
        else:
            return JsonResponse(user.errors, status=400)
    else:
        return HttpResponse("Hello, world! - user op")


def task_op(request):
    return HttpResponse("Hello, world! - task op")


def tasklist_op(request):
    return HttpResponse("Hello, world! - tasklist op")


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

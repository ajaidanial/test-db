from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from testapp.serializers import UserSerializer


@csrf_exempt
def user_op(request):
    if request.method == 'GET':
        try:
            name: str = request.GET['name']
            email: str = request.GET['email']
            return HttpResponse(name + " " + email)
        #     TODO: token auth
        except MultiValueDictKeyError:
            return HttpResponse("user op")
    elif request.method == 'POST':
        user = UserSerializer(data=dict(request.POST.items()))
        if user.is_valid():
            user.save()
            # token = Token.objects.create(user=user)
            return JsonResponse(user.data)
        #     TODO: token auth
        else:
            return JsonResponse(user.errors)
    else:
        return HttpResponse("user op")


def task_op(request):
    return HttpResponse("task op")


def tasklist_op(request):
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

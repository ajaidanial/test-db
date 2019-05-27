from datetime import datetime

from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from testapp.models import *
from testapp.serializers import SnippetSerializer


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
    try:
        return User.objects.prefetch_related(prefetch).get(name=name)
    except AttributeError:
        return User.objects.get(name=name)


def display_task_data_for_user(tasks: dict) -> None:
    for task in tasks:
        print(task)


def create_user(name: str, email: str) -> None:
    user: User = User(name=name, email=email)
    user.save()
    return user.key


@csrf_exempt
def user_op(request):
    if request.method == 'GET':
        name: str = request.GET['name']
        email: str = request.GET['email']
        return HttpResponse(name)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=dict(request.POST.items()))
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data, status=201)
    # return JsonResponse(serializer.errors, status=400)
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

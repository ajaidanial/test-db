from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.renderers import  JSONRenderer
from rest_framework.response import Response
# from requests import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from testapp import database_operations
from testapp.forms import UserForm


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
    if request.method == 'GET':  # Get all tasks
        return JsonResponse(database_operations.get_all_tasks(), safe=False)
    if request.method == 'POST':  # Create new task
        try:
            received_token: str = request.META.get('HTTP_AUTHORIZATION')
            data = json.loads(request.body)

            if not database_operations.is_valid_schema("create_task.json", data):
                return JsonResponse({'success': False, 'required data': 'improper schema'})
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
def task_delete_update_display(request, id):
    received_token: str = request.META.get('HTTP_AUTHORIZATION')
    if request.method == "DELETE":
        return JsonResponse(database_operations.delete_task(id, received_token))
    if request.method == "PUT":
        received_token: str = request.META.get('HTTP_AUTHORIZATION')
        data = json.loads(request.body)
        if data == {}:
            return HttpResponse(None)
        return JsonResponse(database_operations.update_task(data, received_token, id))
    if request.method == 'GET':
        return JsonResponse(database_operations.get_task(id))
    return HttpResponse(None)


@csrf_exempt
def get_update_and_delete_tasklist(request, id):
    received_token: str = request.META.get('HTTP_AUTHORIZATION')
    if request.method == "DELETE":
        return JsonResponse(database_operations.delete_tasklist(id, received_token))
    if request.method == "PUT":
        data = json.loads(request.body)
        if data == {}:
            return HttpResponse(None)
        return JsonResponse(database_operations.update_tasklist(data, received_token, id))
    if request.method == 'GET':
        return JsonResponse(database_operations.get_tasklist(id))
    return HttpResponse(None)


@csrf_exempt
def register_user(request):
    data = json.loads(request.body)
    if not database_operations.is_valid_schema("user.json", data):
        return JsonResponse({'success': False, 'required data': 'improper schema'})
    if request.method == "POST":
        try:
            username: str = data['username']
            password: str = data['password']
            email: str = data['email']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse({'success': False, 'required data': 'username, password, email'})
        user = UserForm(data)
        if user.is_valid():
            return JsonResponse(database_operations.singup_user_and_return_token(username, password, email))
        else:
            return JsonResponse(user.errors)
    else:
        return HttpResponse(None)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if not database_operations.is_valid_schema("login_user.json", data):
                return JsonResponse({'success': False, 'required data': 'improper schema'})

            username: str = data['username']
            password: str = data['password']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse({'success': False, 'required data': 'username, password'})
        return JsonResponse(database_operations.login_user(username, password))
    else:
        return HttpResponse(None)


class LoginUser(APIView):
    authentication_class = TokenAuthentication

    def enforce_csrf(self, request):
        return

    def post(self, request, format=None):
        try:
            data = json.loads(request.body)

            if not database_operations.is_valid_schema("login_user.json", data):
                return JsonResponse({'success': False, 'required data': 'improper schema'})

            username: str = data['username']
            password: str = data['password']
        except MultiValueDictKeyError:
            return HttpResponse(None)
        except KeyError:
            return JsonResponse({'success': False, 'required data': 'username, password'})
        return JsonResponse(database_operations.login_user(username, password))


class APIExtendedView(APIView):
    schema_class = None

    def validate_data(self) -> bool:
        if self.request.method == 'POST' and self.schema_class is not None:
            if not database_operations.is_valid_schema(self.schema_class, self.request.data):
                return False
            else:
                return True

    def send_schema_error_response(self):
        return JsonResponse({'success': False, 'error': 'Improper schema'})


class GetAllAndCreateTaskList(APIExtendedView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    parser_classes = (JSONParser, FormParser)
    renderer_classes = (JSONRenderer, )
    schema_class = "tasklist.json"

    def enforce_csrf(self, request):
        return

    def get(self, request, format=None):
        return Response(database_operations.get_all_tasklist())

    def post(self, request, format=None):
        if not self.validate_data():
            return self.send_schema_error_response()
        # received_token: str = request.auth
        # data = json.loads(request.body)
        # data = request.data
        # if not database_operations.is_valid_schema("tasklist.json", data):
        #     return JsonResponse({'success': False, 'required data': 'improper schema'})

        # try:
        #     name: str = data['name']
        #     creator: str = data['creator']
        # except MultiValueDictKeyError:
        #     return HttpResponse({"success": False, "required data": "name, creator"})
        return JsonResponse(database_operations.create_tasklist(**request.data, user=request.user))

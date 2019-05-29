from django.urls import path

from testapp import views

urlpatterns = [
    path('', views.user_op, name='user operations'),
    path('tasklist', views.tasklist_op, name='tasklist operations'),

    path('task', views.task_op, name='tasks info'),
    path('task/<int:id>', views.task_delete_update, name='delete task'),
    path('register/', views.register_user, name='register user'),
    path('login/', views.login_user, name='login user'),
]

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

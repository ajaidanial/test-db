from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_op, name='user operations'),
    path('tasklist', views.tasklist_op, name='tasklist operations'),
    path('task', views.task_op, name='task operations'),
]

"""
user op
    - login (token)
    - register (tokeb)

tasklist
    - create
    - delete

task
    - delete
    - create
    - get all tasks for user
    - close task
"""

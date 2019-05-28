from django.urls import path

from testapp import views

urlpatterns = [
    path('', views.user_op, name='user operations'),
    path('tasklist', views.tasklist_op, name='tasklist operations'),
    path('task', views.task_op, name='task operations'),
]

from django.urls import path

from testapp import views

urlpatterns = [
    path('', views.user_op, name='user operations'),
    path('tasklist', views.tasklist_op, name='tasklist operations'),

    path('tasks', views.task_op, name='tasks info'),
    path('task/<int:id>', views.task_delete_update, name='delete task'),
    path('register/', views.register_user, name='register user'),  # Done
    path('login/', views.login_user, name='login user'),  # Done
]

"""
serializer
urls
task
list of data
hyperlinks
task_display all data
json boolean
tasklist based segregation
instance2dict -> serializer
change everything to id
make id as primary key
"""

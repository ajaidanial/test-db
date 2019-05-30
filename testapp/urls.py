from django.urls import path

from testapp import views

urlpatterns = [
    path('', views.user_op, name='user operations'),
    # path('tasklist', views.tasklist_op, name='tasklist operations'),

    path('tasks', views.task_op, name='tasks info'),  # Done
    path('task/<int:id>', views.task_delete_update_display, name='delete, update and view a task'),  # Done
    path('register/', views.register_user, name='register user'),  # Done
    path('login/', views.login_user, name='login user'),  # Done
    path('tasklist/<int:id>', views.get_update_and_delete_tasklist, name='view, update and delete a tasklist'),
    path('tasklists/', views.get_all_tasklists, name='get all tasklists'),
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
# update tasklist = put

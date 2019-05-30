from rest_framework import serializers

from testapp.models import User, TaskList, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class TaskListSerializer(serializers.ModelSerializer):
    creator = UserSerializer()

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'created_date', "creator")


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True)
    task_list = TaskListSerializer()

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'created_date',
            'due_date',
            'is_open',
            "creator",
            "assigned_users",
            "task_list",
        )

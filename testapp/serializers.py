from rest_framework import serializers

from testapp.models import User, TaskList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ('name', 'created_date', "creator")

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=300, default='test')

    def __str__(self):
        return self.username


class Task(models.Model):
    name = models.CharField(max_length=300, unique=True)
    created_date = models.DateField()
    due_date = models.DateField()
    is_open = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks')
    task_list = models.ForeignKey('TaskList', related_name='task_list', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def update_field(self, key, value):
        # This will raise an AttributeError if the key isn't an attribute
        # of your model
        getattr(self, key)
        setattr(self, key, value)


class TaskList(models.Model):
    name = models.CharField(max_length=300, unique=True)
    created_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def update_field(self, key, value):
        # This will raise an AttributeError if the key isn't an attribute
        # of your model
        getattr(self, key)
        setattr(self, key, value)

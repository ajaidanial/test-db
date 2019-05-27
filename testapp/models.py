from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, default='test@test.com')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    created_date = models.DateField()
    due_date = models.DateField()
    is_open = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks')
    task_list = models.ForeignKey('TaskList', related_name='task_list', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskList(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    created_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

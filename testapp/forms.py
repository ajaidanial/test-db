from django.forms import ModelForm

from testapp.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class TaskListForm(ModelForm):
#     creator = forms.ModelMultipleChoiceField(queryset=User.objects.all())
#
#     class Meta:
#         def __init__(self, *args, **kwargs):
#             super(TaskListForm, self).__init__(*args, **kwargs)
#             self.fields['creator'] = forms.ModelChoiceField(
#                 queryset=User.objects.all())
#
#         model = TaskList
#         fields = ['name', 'created_date', "creator"]

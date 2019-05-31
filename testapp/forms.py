from django.forms import ModelForm

from testapp.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

from rest_framework import serializers

from testapp.models import User


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')

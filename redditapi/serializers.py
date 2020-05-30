from rest_framework import serializers

from django.contrib.auth.models import User

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class RedditSerializer(serializers.ModelSerializer):
    class Meta:
        model = redditdata
        fields = "__all__"


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = redditdata
        fields = "__all__"


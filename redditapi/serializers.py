from rest_framework import serializers


from .models import *


class RedditSerializer(serializers.ModelSerializer):
    class Meta:
        model = redditdata
        fields = "__all__"


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = redditdata
        fields = "__all__"
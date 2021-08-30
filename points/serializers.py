from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        depth = 1

class InterestPointSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.InterestPoint
        fields = ['id', 'name', 'longitude', 'latitude', 'user']
        


class SharedInterestSerializer(serializers.ModelSerializer):
    shared_user = UserSerializer(read_only=True)
    interest = InterestPointSerializer(read_only=True)
    class Meta:
        model = models.SharedInterest
        fields = ['id', 'interest', 'shared_user']




from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Customer
        fields = '__all__'  # Include all fields, including balance

class CustomerCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Customer
        exclude = ['balance', 'account_no']




class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        doctor = models.Manager.objects.create(user=user, **validated_data)
        return doctor

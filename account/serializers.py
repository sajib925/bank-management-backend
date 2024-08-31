from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

# Serializer for retrieving customer data, including the balance field
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Customer
        fields = '__all__'  # Include all fields, including balance

# Serializer for creating customer data, excluding the balance field
class CustomerCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Customer
        exclude = ['balance']  # Exclude the balance field during creation




class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        doctor = models.Manager.objects.create(user=user, **validated_data)
        return doctor

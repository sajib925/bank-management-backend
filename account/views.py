from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . import models, serializers
from rest_framework.permissions import IsAuthenticated

class ManagerListCreateApiView(APIView):
    def get(self, request):
        manager = models.Manager.objects.all()
        serializer = serializers.ManagerSerializer(manager, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ManagerSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerDetailApiView(APIView):
    def get(self, request, pk):
        doctor = get_object_or_404(models.Manager, pk=pk)
        serializer = serializers.ManagerSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        manager = get_object_or_404(models.Manager, pk=pk)
        serializer = serializers.ManagerSerializer(manager, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manager = get_object_or_404(models.Manager, pk=pk)
        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerCreateApiView(APIView):
    def get(self, request):
        customer = models.Customer.objects.all()
        serializer = serializers.CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id

        # Explicitly set the balance to '0' during creation
        data = request.data.copy()
        data['balance'] = '0'

        serializer = serializers.CustomerCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailApiView(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(models.Customer, pk=pk)
        serializer = serializers.CustomerSerializer(customer)
        return Response(serializer.data)

    def patch(self, request, pk):
        customer = get_object_or_404(models.Customer, pk=pk)
        serializer = serializers.CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(models.Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





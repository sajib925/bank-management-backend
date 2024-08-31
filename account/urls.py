from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.ManagerListCreateApiView.as_view(), name='admin_user-list-create'),
    path('manager/<int:pk>/', views.ManagerDetailApiView.as_view(), name='admin_user-detail'),
    path('customer/', views.CustomerCreateApiView.as_view(), name='normal_user-list-create'),
    path('customer/<int:pk>/', views.CustomerDetailApiView.as_view(), name='normal_user-detail'),
]




from django.urls import path
from .views import UserRegistrationApiView, UserLoginApiView, UserLogoutView, PasswordUpdateView,ProfileUpdateView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('update-password/', PasswordUpdateView.as_view(), name='update_password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]

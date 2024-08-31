from django.db import models
from django.contrib.auth.models import User
from .constants import RELIGION_CHOICES, ACCOUNT_TYPE_CHOICES

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.CharField(max_length=12, null=True, blank=True, default='0')
    mobile_no = models.CharField(max_length=12)
    nid = models.CharField(max_length=12, unique=True)
    age = models.CharField(max_length=5)
    monthly_income = models.CharField(max_length=10)
    # religion = models.CharField(max_length=15, choices=RELIGION_CHOICES)
    # account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=12)
    nid = models.CharField(max_length=12, unique=True)
    age = models.CharField(max_length=5)
    # religion = models.CharField(max_length=15, choices=RELIGION_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  # This is correct

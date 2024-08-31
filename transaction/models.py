


from django.db import models
from django.contrib.auth.models import User
from .constants import TRANSACTION_TYPE, LOAN_PAID

class Transaction(models.Model):


    account = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approved = models.BooleanField(default=False)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == LOAN_PAID:
            self.loan_approved = True
        super().save(*args, **kwargs)

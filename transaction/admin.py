from django.contrib import admin
from .models import Transaction,Loan, Deposit, Withdrawal, BalanceTransfer

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(BalanceTransfer)
admin.site.register(Deposit)
admin.site.register(Withdrawal)

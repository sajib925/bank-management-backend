from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from .constants import TRANSACTION_TYPE, LOAN_PAID
from account.models import Customer, Manager


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



class BalanceTransfer(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_transfers', on_delete=models.CASCADE)
    recipient_account_no = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.sender.user.username} to {self.recipient_account_no} - {self.amount}"

    def save(self, *args, **kwargs):
            # Ensure the sender has enough balance
        if Decimal(self.sender.balance) < self.amount:
            raise ValueError("Insufficient balance")

            # Deduct the amount from sender's balance
        self.sender.balance = str(Decimal(self.sender.balance) - self.amount)
        self.sender.save()

            # Find the recipient by account number and add the amount to their balance
        try:
            recipient = Customer.objects.get(account_no=self.recipient_account_no)
            recipient.balance = str(Decimal(recipient.balance) + self.amount)
            recipient.save()
        except Customer.DoesNotExist:
            raise ValueError("Recipient account number not found")

        super().save(*args, **kwargs)


class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Loan Request by {self.customer.user.username} - {self.status}"

    def approve_loan(self, manager, amount_approved):
        """Manager approves the loan, setting the amount approved and updating the customer's balance."""
        if self.status != 'pending':
            raise ValueError("Loan has already been processed.")
        self.manager = manager
        self.amount_approved = amount_approved
        self.status = 'approved'
        self.approval_date = timezone.now()
        # Update customer's balance
        self.customer.balance = str(Decimal(self.customer.balance) + amount_approved)
        self.customer.save()
        self.save()

    def reject_loan(self, manager):
        """Manager rejects the loan, updating the status and recording the rejection date."""
        if self.status != 'pending':
            raise ValueError("Loan has already been processed.")
        self.manager = manager
        self.status = 'rejected'
        self.approval_date = timezone.now()
        self.save()

    def repay_loan(self, amount):
        """Customer repays the loan, decreasing the balance."""
        if self.status != 'approved':
            raise ValueError("Loan must be approved to be repaid.")

        # Convert amount to Decimal if it's not already
        amount = Decimal(amount)

        if amount <= 0:
            raise ValueError("Repayment amount must be positive.")

        if Decimal(self.customer.balance) < amount:
            raise ValueError("Insufficient balance to repay the loan.")

        # Decrease customer's balance
        self.customer.balance = str(Decimal(self.customer.balance) - amount)
        self.customer.save()

        # Decrease the loan balance or mark it as paid off
        self.amount_approved = str(Decimal(self.amount_approved) - amount)

        # If the loan is fully paid off
        if Decimal(self.amount_approved) <= 0:
            self.status = 'paid'
            self.amount_approved = '0'

        self.save()



class Withdrawal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal by {self.customer.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        # Ensure the customer has enough balance
        if Decimal(self.customer.balance) < self.amount:
            raise ValueError("Insufficient balance")

        # Subtract the withdrawal amount from the customer's balance
        self.customer.balance = str(Decimal(self.customer.balance) - self.amount)
        self.customer.save()
        super().save(*args, **kwargs)




# class Deposit(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     # manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Deposit by {self.customer.user.username} - {self.amount}"
#
#     def save(self, *args, **kwargs):
#         # Add the deposit amount to the customer's balance
#         self.customer.balance = str(Decimal(self.customer.balance) + self.amount)
#         self.customer.save()
#         super().save(*args, **kwargs)


# class Deposit(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     transaction_id = models.CharField(max_length=255, unique=True, null=True)
#     status = models.CharField(max_length=20, default='pending')  # Track the status of the deposit
#
#     def __str__(self):
#         return f"Deposit by {self.customer.user.username} - {self.amount}"
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)  # Save the deposit instance first
#         if self.status == 'completed':
#             # Only update the balance if the status is completed
#             self.customer.balance = str(Decimal(self.customer.balance) + self.amount)
#             self.customer.save()

class Deposit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return f"Deposit by {self.customer.user.username} - {self.amount} ({self.status})"

    def complete_deposit(self):
        """
        Finalizes the deposit by updating the customer's balance if the status is 'COMPLETED'.
        """
        if self.status == 'COMPLETED':
            self.customer.balance = str(Decimal(self.customer.balance) + self.amount)
            self.customer.save()
            super().save()

    def save(self, *args, **kwargs):
        # Override save to prevent balance updates if status is not 'COMPLETED'
        if self.status == 'COMPLETED':
            self.complete_deposit()
        else:
            super().save(*args, **kwargs)


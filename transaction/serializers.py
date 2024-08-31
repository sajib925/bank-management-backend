from decimal import Decimal
from rest_framework import serializers
from .models import Transaction
from .constants import TRANSACTION_TYPE


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'transaction_type', 'timestamp', 'loan_approved', 'balance_after_transaction']

    def validate_amount(self, value):
        if not isinstance(value, (int, float, Decimal)):
            raise serializers.ValidationError("Amount must be a number.")
        return value

    def validate_transaction_type(self, value):
        if value not in dict(TRANSACTION_TYPE).keys():
            raise serializers.ValidationError("Invalid transaction type.")
        return value

from decimal import Decimal
from rest_framework import serializers
from .models import Transaction, Loan
from .constants import TRANSACTION_TYPE
from account.models import Customer


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




class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount_requested', 'amount_approved', 'status', 'request_date']
        extra_kwargs = {
            'amount_approved': {'read_only': True},
            'status': {'read_only': True},
            'request_date': {'read_only': True},
        }


from .models import BalanceTransfer, Loan, Deposit, Withdrawal



class BalanceTransferSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()

    class Meta:
        model = BalanceTransfer
        fields = '__all__'
        read_only_fields = ['sender']  # Ensure 'sender' is read-only to the client

    def get_sender_name(self, obj):
        return obj.sender.user.get_full_name() if obj.sender else None

    def get_recipient_name(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.user.get_full_name()
        except Customer.DoesNotExist:
            return "Unknown Recipient"

    def create(self, validated_data):
        sender = self.context['request'].user.customer  # Automatically set the sender
        validated_data['sender'] = sender

        # Ensure the sender has enough balance
        if Decimal(sender.balance) < validated_data['amount']:
            raise serializers.ValidationError("Insufficient balance")

        # Deduct the amount from sender's balance
        sender.balance = str(Decimal(sender.balance) - validated_data['amount'])
        sender.save()

        # Find the recipient by account number and add the amount to their balance
        try:
            recipient = Customer.objects.get(account_no=validated_data['recipient_account_no'])
            recipient.balance = str(Decimal(recipient.balance) + validated_data['amount'])
            recipient.save()
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Recipient account number not found")

        return super().create(validated_data)


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['customer']

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)



class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ['customer']  # Make customer field read-only

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'
        read_only_fields = ['customer']

    def create(self, validated_data):
        customer = self.context['request'].user.customer  # Automatically set the customer
        validated_data['customer'] = customer
        return super().create(validated_data)



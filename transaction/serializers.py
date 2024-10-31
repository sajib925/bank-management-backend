from decimal import Decimal
from rest_framework import serializers
from .models import Transaction, Loan
from .constants import TRANSACTION_TYPE
from account.models import Customer
from .models import BalanceTransfer, Loan, Deposit, Withdrawal


class BalanceTransferSerializer(serializers.ModelSerializer):
    # Sender details
    sender_name = serializers.SerializerMethodField()
    sender_email = serializers.SerializerMethodField()
    sender_mobile_no = serializers.SerializerMethodField()
    sender_image = serializers.SerializerMethodField()
    sender_account_no = serializers.SerializerMethodField()
    sender_account_type = serializers.SerializerMethodField()

    # Recipient details
    recipient_name = serializers.SerializerMethodField()
    recipient_email = serializers.SerializerMethodField()
    recipient_mobile_no = serializers.SerializerMethodField()
    recipient_image = serializers.SerializerMethodField()
    recipient_account_no = serializers.SerializerMethodField()
    recipient_account_type = serializers.SerializerMethodField()

    class Meta:
        model = BalanceTransfer
        fields = '__all__'
        read_only_fields = ['sender']  # Ensure 'sender' is read-only to the client

    # Sender related methods
    def get_sender_name(self, obj):
        return obj.sender.user.get_full_name() if obj.sender else None

    def get_sender_email(self, obj):
        return obj.sender.user.email if obj.sender else None

    def get_sender_mobile_no(self, obj):
        return obj.sender.mobile_no if obj.sender else None

    def get_sender_image(self, obj):
        return obj.sender.image if obj.sender else None

    def get_sender_account_no(self, obj):
        return obj.sender.account_no if obj.sender else None

    def get_sender_account_type(self, obj):
        return obj.sender.account_type if obj.sender else None

    # Recipient related methods
    def get_recipient_name(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.user.get_full_name()
        except Customer.DoesNotExist:
            return "Unknown Recipient"

    def get_recipient_email(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.user.email
        except Customer.DoesNotExist:
            return "Unknown Recipient Email"

    def get_recipient_mobile_no(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.mobile_no
        except Customer.DoesNotExist:
            return "Unknown Recipient Mobile No"

    def get_recipient_image(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.image
        except Customer.DoesNotExist:
            return "Unknown Recipient Image"

    def get_recipient_account_no(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.account_no
        except Customer.DoesNotExist:
            return "Unknown Recipient Account No"

    def get_recipient_account_type(self, obj):
        try:
            recipient = Customer.objects.get(account_no=obj.recipient_account_no)
            return recipient.account_type
        except Customer.DoesNotExist:
            return "Unknown Recipient Account Type"

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
    customer_name = serializers.CharField(source='customer.user.get_full_name', read_only=True)
    customer_email = serializers.EmailField(source='customer.user.email', read_only=True)
    customer_mobile_no = serializers.CharField(source='customer.mobile_no', read_only=True)
    customer_account_no = serializers.CharField(source='customer.account_no', read_only=True)
    customer_account_type = serializers.CharField(source='customer.account_type', read_only=True)
    customer_image = serializers.CharField(source='customer.image', read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'amount_requested', 'amount_approved', 'status', 'request_date',
                  'approval_date', 'customer_name', 'customer_email', 'customer_mobile_no', 'customer_account_type', 'customer_image', 'customer_account_no']
        read_only_fields = ['customer', 'status', 'approval_date', 'manager']

    def create(self, validated_data):
        # Automatically associate the loan with the current customer
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)


class WithdrawalSerializer(serializers.ModelSerializer):
    # Add customer details
    customer_name = serializers.CharField(source='customer.user.get_full_name', read_only=True)
    customer_email = serializers.EmailField(source='customer.user.email', read_only=True)
    customer_mobile_no = serializers.CharField(source='customer.mobile_no', read_only=True)
    customer_account_no = serializers.CharField(source='customer.account_no', read_only=True)
    customer_account_type = serializers.CharField(source='customer.account_type', read_only=True)
    customer_image = serializers.CharField(source='customer.image', read_only=True)

    class Meta:
        model = Withdrawal
        fields = ['id', 'amount', 'timestamp', 'customer_name', 'customer_email', 'customer_mobile_no', 'customer_account_type', 'customer_image', 'customer_account_no']
        read_only_fields = ['customer']

    def create(self, validated_data):
        # Automatically associate the withdrawal with the current customer
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)


class DepositSerializer(serializers.ModelSerializer):
    # Add customer details
    customer_name = serializers.CharField(source='customer.user.get_full_name', read_only=True)
    customer_email = serializers.EmailField(source='customer.user.email', read_only=True)
    customer_mobile_no = serializers.CharField(source='customer.mobile_no', read_only=True)
    customer_account_no = serializers.CharField(source='customer.account_no', read_only=True)
    customer_account_type = serializers.CharField(source='customer.account_type', read_only=True)
    customer_image = serializers.CharField(source='customer.image', read_only=True)

    class Meta:
        model = Deposit
        fields = ['id', 'amount', 'timestamp', 'customer_name', 'customer_email', 'customer_mobile_no', 'customer_account_type', 'customer_image', 'customer_account_no']
        read_only_fields = ['customer']

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)


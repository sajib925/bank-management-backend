from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Transaction
from account.models import Customer
from .serializers import TransactionSerializer
from .constants import LOAN_PAID, LOAN

class DepositMoneyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Create a copy of request data
        data['account'] = request.user.id  # Set the account field to the current user

        try:
            # Convert amount to Decimal if it's a string
            if isinstance(data.get('amount'), str):
                data['amount'] = Decimal(data['amount'])
        except (ValueError, InvalidOperation):
            return Response({"amount": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            transaction = serializer.save()

            # Add the deposited amount to the user's balance
            user_account = Customer.objects.get(user=request.user)
            user_account.balance = Decimal(user_account.balance) + transaction.amount
            user_account.save(update_fields=['balance'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawMoneyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['account'] = request.user.id  # Set the account field to the current user

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            amount = serializer.validated_data.get('amount')
            user_account = Customer.objects.get(user=request.user)

            # Check if the user has sufficient balance
            if amount > Decimal(user_account.balance):
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct the amount from the user's balance
            user_account.balance = Decimal(user_account.balance) - amount
            user_account.save(update_fields=['balance'])

            # Save the transaction
            serializer.save()

            return Response({'message': 'Withdrawal successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['account'] = request.user.id  # Set the account field to the current user

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            amount = serializer.validated_data.get('amount')
            current_loan_count = Transaction.objects.filter(
                account=request.user,
                transaction_type=LOAN,
                loan_approved=True
            ).count()

            if current_loan_count >= 3:
                return Response({'error': 'Loan limit exceeded'}, status=status.HTTP_400_BAD_REQUEST)

            # Process loan request
            # ...

            return Response({'message': 'Loan request submitted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PayLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        if loan.loan_approved:
            user_account = Customer.objects.get(user=loan.account)  # Assuming `account` is a User model

            if loan.amount <= Decimal(user_account.balance):
                user_account.balance = Decimal(user_account.balance) - loan.amount
                user_account.save(update_fields=['balance'])

                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()

                return Response({'message': 'Loan paid successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Loan not approved'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionReportView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        queryset = Transaction.objects.filter(account=self.request.user)

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

        return queryset.distinct()

class LoanListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            account=self.request.user,
            transaction_type=LOAN
        )


class ApproveLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        if loan.transaction_type != LOAN:
            return Response({'error': 'Not a loan transaction'}, status=status.HTTP_400_BAD_REQUEST)

        if loan.loan_approved:
            return Response({'error': 'Loan already approved'}, status=status.HTTP_400_BAD_REQUEST)

        # Approve the loan
        loan.loan_approved = True
        loan.save()

        return Response({'message': 'Loan approved successfully'}, status=status.HTTP_200_OK)

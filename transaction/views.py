from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import BalanceTransfer, Loan, Deposit, Withdrawal
from .serializers import BalanceTransferSerializer, LoanSerializer, DepositSerializer, WithdrawalSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from account.models import Customer, Manager
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal, InvalidOperation
from django.conf import settings
from decimal import Decimal
from rest_framework.views import APIView
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from decimal import Decimal
from libs.payment_request import payment_request
from libs.auto_transaction_id_generate import generate_transaction_id
from libs.live_link import frontend_link


class BalanceTransferCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'manager'):
            # If the user is a manager, return all balance transfers
            transfers = BalanceTransfer.objects.all()
        else:
            # If the user is a customer, return only their balance transfers
            try:
                customer = get_object_or_404(Customer, user=user)
                transfers = BalanceTransfer.objects.filter(sender=customer)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BalanceTransferSerializer(transfers, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Set sender and perform balance transfer
        try:
            serializer = BalanceTransferSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                # Perform additional validation if needed
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if hasattr(user, 'manager'):
            # If the user is a manager, return all loans
            loans = Loan.objects.select_related('customer__user').all()
        elif hasattr(user, 'customer'):
            # If the user is a customer, return only their loans
            loans = Loan.objects.filter(customer=user.customer)
        else:
            return Response({'detail': 'User type not recognized.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = LoanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanDetailView(APIView):
    def get(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        serializer = LoanSerializer(loan)
        return Response(serializer.data)

    def put(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        serializer = LoanSerializer(loan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoanApproveView(APIView):
    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        amount_approved = request.data.get('amount_approved')

        if amount_approved is not None:
            try:
                amount_approved = Decimal(amount_approved)
            except (ValueError, InvalidOperation):
                return Response({"amount_approved": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the user is a Manager
            if not hasattr(request.user, 'manager'):
                return Response({"detail": "You do not have permission to approve loans."},
                                status=status.HTTP_403_FORBIDDEN)

            # Get the Manager instance
            manager = request.user.manager

            # Call the approve_loan method with the correct Manager instance
            loan.approve_loan(manager=manager, amount_approved=amount_approved)
            return Response(LoanSerializer(loan).data)

        return Response({"amount_approved": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)


class LoanRejectView(APIView):
    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)

        # Ensure the user is a Manager
        if not hasattr(request.user, 'manager'):
            return Response({"detail": "You do not have permission to reject loans."},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the Manager instance
        manager = request.user.manager

        # Call the reject_loan method with the correct Manager instance
        try:
            loan.reject_loan(manager=manager)
            # Use a serializer to return relevant data (optional)
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoanRepayView(APIView):
    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        amount = request.data.get('amount')
        try:
            loan.repay_loan(amount)
            return Response({"status": "Loan repaid successfully"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'manager'):
            # User is a Manager, so show all withdrawals
            withdrawals = Withdrawal.objects.select_related('customer__user').all()
        else:
            # User is a Customer, so show only their withdrawals
            customer = request.user.customer
            withdrawals = Withdrawal.objects.filter(customer=customer)

        serializer = WithdrawalSerializer(withdrawals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'manager'):
            deposits = Deposit.objects.select_related('customer__user').all()
        else:
            customer = get_object_or_404(Customer, user=user)
            deposits = Deposit.objects.filter(customer=customer)

        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)

    # without payment gateway

    # def post(self, request):
    #     serializer = DepositSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # with payment gateway

    def post(self, request):
        # Get the customer associated with the logged-in user
        customer = self.request.user.customer
        serializer = DepositSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Create a Deposit instance but do not save yet
            deposit = serializer.save(customer=customer)
            url = payment_request(deposit.amount, self.request.user)

            # Return the response with the updated balance and payment URL
            return Response({
                'balance': customer.balance,
                'payment_url': url
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DepositSuccess(APIView):
    def post(self, request, *args, **kwargs):
        # user_id = request.data.get('value_a')
        amount = float(request.data.get('amount'))  # Ensure you parse the amount correctly
        tran_id = request.data.get('tran_id')

        # Safely retrieve the user and associated customer
        # user = get_object_or_404(User, id=user_id)
        customer = get_object_or_404(Customer, user=user)

        # Update the customer's balance
        customer.balance = str(Decimal(customer.balance) + Decimal(amount))
        customer.save(update_fields=['balance'])

        # Create a Deposit instance
        deposit = Deposit(customer=customer, amount=amount)
        deposit.save()  # Save the deposit record in the database


        return HttpResponseRedirect(f'{frontend_link}/transaction?status=success')




class DepositFailed(APIView):
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(f'{frontend_link}/fail?status=failed')

class DepositCancelled(APIView):
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(f'{frontend_link}/cancel?status=cancelled')
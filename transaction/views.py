from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BalanceTransfer, Loan, Deposit, Withdrawal
from .serializers import BalanceTransferSerializer, LoanSerializer, DepositSerializer, WithdrawalSerializer, PaymentInitiateSerializer, PaymentStatusSerializer
from django.shortcuts import get_object_or_404
from account.models import Customer, Manager
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal, InvalidOperation
from django.conf import settings
from decimal import Decimal
from rest_framework.views import APIView
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from decimal import Decimal
from .models import Deposit, Customer




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




class DepositCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Check if the user is a manager
        if hasattr(user, 'manager'):
            # If the user is a manager, return all deposits with customer details
            deposits = Deposit.objects.select_related('customer__user').all()
        else:
            # If the user is a customer, return only their deposits
            customer = get_object_or_404(Customer, user=user)
            deposits = Deposit.objects.filter(customer=customer)

        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = DepositSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = DepositSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


class InitiatePaymentView(APIView):
    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if serializer.is_valid():
            sslcz = SSLCOMMERZ(settings.SSLCOMMERZ)
            amount = serializer.validated_data['amount']
            customer_id = serializer.validated_data['customer_id']
            customer = Customer.objects.get(id=customer_id)

            post_body = {
                'total_amount': amount,
                'currency': 'BDT',
                'tran_id': f'trans_{customer_id}_{amount}',  # Unique transaction ID
                'success_url': settings.SSLCOMMERZ_SUCCESS_URL,
                'fail_url': settings.SSLCOMMERZ_FAIL_URL,
                'cancel_url': settings.SSLCOMMERZ_CANCEL_URL,
                'cus_name': customer.user.username,
                'cus_email': customer.user.email,
                'cus_phone': customer.phone_number,
                'cus_add1': "Dhaka Bangladesh",
                'cus_city': "Dhaka",
                'cus_country': 'Bangladesh',
            }

            response = sslcz.createSession(post_body)
            if response['status'] == 'SUCCESS':
                return Response({'payment_url': response['GatewayPageURL']})
            return Response({'error': 'Payment initiation failed'}, status=400)
        return Response(serializer.errors, status=400)


class PaymentSuccessView(APIView):
    def post(self, request):
        serializer = PaymentStatusSerializer(data=request.data)
        if serializer.is_valid():
            sslcz = SSLCOMMERZ(settings.SSLCOMMERZ)
            val_id = serializer.validated_data['val_id']
            response = sslcz.validationTransactionOrder(val_id)

            if response['status'] == 'VALID':
                customer = Customer.objects.get(id=serializer.validated_data["customer_id"])
                amount = Decimal(response['amount'])
                Deposit.objects.create(customer=customer, amount=amount,
                                       transaction_id=serializer.validated_data["tran_id"])
                return Response({'status': 'Payment successful'})
            return Response({'error': 'Payment validation failed'}, status=400)
        return Response(serializer.errors, status=400)


class PaymentFailureView(APIView):
    def post(self, request):
        return Response({'error': 'Payment failed'}, status=400)


class PaymentCancelView(APIView):
    def post(self, request):
        return Response({'status': 'Payment was canceled'}, status=200)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BalanceTransfer, Loan, Deposit, Withdrawal
from .serializers import BalanceTransferSerializer, LoanSerializer, DepositSerializer, WithdrawalSerializer
from django.shortcuts import get_object_or_404
from account.models import Customer, Manager
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal, InvalidOperation
from django.conf import settings
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.urls import reverse




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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        amount = request.data.get('amount')

        # SSLCommerz payment initialization
        sslcz = SSLCSession(
            sslcommerz_settings={
                'store_id': settings.SSL_COMMERZ_STORE_ID,
                'store_pass': settings.SSL_COMMERZ_STORE_PASSWORD,
                'issandbox': True  # Set to False in production
            }
        )

        # Prepare the transaction parameters
        sslcz.set_urls(
            success_url=request.build_absolute_uri(reverse('payment-success')),
            fail_url=request.build_absolute_uri(reverse('payment-failure')),
            cancel_url=request.build_absolute_uri(reverse('payment-failure')),
            ipn_url=request.build_absolute_uri(reverse('payment-ipn'))
        )

        sslcz.set_product_integration(
            total_amount=Decimal(amount),
            currency='BDT',
            product_category='Deposit',
            product_name='Account Deposit',
            num_of_item=1,
            shipping_method='No',
            product_profile='general'
        )

        sslcz.set_customer_info(
            name=customer.user.get_full_name(),
            email=customer.user.email,
            address1="Dhaka, Bangladesh",
            city="Dhaka",
            postcode="1200",
            country="Bangladesh",
            phone=customer.mobile_no
        )

        # Initiate payment and get response
        response = sslcz.init_payment()
        if response.get('status') == 'SUCCESS':
            # Save the transaction ID for reference
            deposit = Deposit.objects.create(
                customer=customer,
                amount=Decimal(amount),
                transaction_id=response['sessionkey']
            )
            return Response({'GatewayPageURL': response['GatewayPageURL']}, status=status.HTTP_200_OK)

        return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        deposit = get_object_or_404(Deposit, transaction_id=transaction_id)
        deposit.save()  # Add amount to customer's balance upon success
        return Response({'message': 'Payment successful', 'deposit': DepositSerializer(deposit).data},
                        status=status.HTTP_200_OK)


class PaymentFailureView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        deposit = get_object_or_404(Deposit, transaction_id=transaction_id)
        deposit.delete()  # Delete the failed deposit
        return Response({'message': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
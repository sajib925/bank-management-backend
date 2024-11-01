from django.urls import path
from .views import (
    BalanceTransferCreateView,
    LoanListCreateView,
    LoanDetailView,
    LoanApproveView,
    LoanRejectView,
    LoanRepayView,
    DepositCreateView,
    # SSLCommerzCallbackView,
    WithdrawalCreateView
)

urlpatterns = [
    path('balance-transfer/', BalanceTransferCreateView.as_view(), name='balance-transfer-create'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:pk>/approve/', LoanApproveView.as_view(), name='loan-approve'),
    path('loans/<int:pk>/reject/', LoanRejectView.as_view(), name='loan-reject'),
    path('loans/<int:pk>/repay/', LoanRepayView.as_view(), name='loan-repay'),
    path('deposit/', DepositCreateView.as_view(), name='deposit-create'),
    # path('sslcommerz/callback/', SSLCommerzCallbackView.as_view(), name='sslcommerz_callback'),
    path('withdrawal/', WithdrawalCreateView.as_view(), name='withdrawal-create'),
]

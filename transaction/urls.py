from django.urls import path
from .views import (
    BalanceTransferCreateView,
    LoanListCreateView,
    LoanDetailView,
    LoanApproveView,
    LoanRejectView,
    LoanRepayView,
    DepositCreateView,
    WithdrawalCreateView,
    DepositCreateView,
    DepositCompleteView,
    DepositFailView,
    DepositCancelView
)

urlpatterns = [
    path('balance-transfer/', BalanceTransferCreateView.as_view(), name='balance-transfer-create'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:pk>/approve/', LoanApproveView.as_view(), name='loan-approve'),
    path('loans/<int:pk>/reject/', LoanRejectView.as_view(), name='loan-reject'),
    path('loans/<int:pk>/repay/', LoanRepayView.as_view(), name='loan-repay'),
    # path('deposit/', DepositCreateView.as_view(), name='deposit-create'),
    path('withdrawal/', WithdrawalCreateView.as_view(), name='withdrawal-create'),
    path('deposit/', DepositCreateView.as_view(), name='deposit'),
    path('deposit/complete/<str:transaction_id>/', DepositCompleteView.as_view(), name='deposit_complete'),
    path('deposit/fail/<str:transaction_id>/', DepositFailView.as_view(), name='deposit_fail'),
    path('deposit/cancel/<str:transaction_id>/', DepositCancelView.as_view(), name='deposit_cancel'),
]

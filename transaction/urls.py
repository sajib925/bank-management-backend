from django.urls import path
from .views import (
    DepositMoneyView,
    WithdrawMoneyView,
    LoanRequestView,
    TransactionReportView,
    PayLoanView,
    LoanListView,
    ApproveLoanView
)

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit-money'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw-money'),
    path('loan/request/', LoanRequestView.as_view(), name='loan-request'),
    path('report/', TransactionReportView.as_view(), name='transaction-report'),
    path('loan/pay/<int:loan_id>/', PayLoanView.as_view(), name='pay-loan'),
    path('loan/list/', LoanListView.as_view(), name='loan-list'),
    path('approve-loan/<int:loan_id>/', ApproveLoanView.as_view(), name='approve-loan'),
]



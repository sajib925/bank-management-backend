# from django.urls import path
# from .views import (
#     DepositMoneyView,
#     WithdrawMoneyView,
#     LoanRequestView,
#     TransactionReportView,
#     PayLoanView,
#     # LoanListView,
#     # ApproveLoanView,
#     LoanList,
#     ApproveLoan,
#     LoanDetail
# )
#
# urlpatterns = [
#     path('deposit/', DepositMoneyView.as_view(), name='deposit-money'),
#     path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw-money'),
#     path('loan/request/', LoanRequestView.as_view(), name='loan-request'),
#     path('report/', TransactionReportView.as_view(), name='transaction-report'),
#     path('loan/pay/<int:loan_id>/', PayLoanView.as_view(), name='pay-loan'),
#     # path('loan/list/', LoanListView.as_view(), name='loan-list'),
#     # path('approve-loan/<int:loan_id>/', ApproveLoanView.as_view(), name='approve-loan'),
#     path('loans/', LoanList.as_view(), name='loan-list'),
#     path('loans/<int:pk>/', LoanDetail.as_view(), name='loan-detail'),
#     path('loans/approve/<int:pk>/', ApproveLoan.as_view(), name='approve-loan'),
# ]
#
#


from django.urls import path
from .views import (
    BalanceTransferCreateView,
    LoanListCreateView,
    LoanDetailView,
    LoanApproveView,
    LoanRejectView,
    LoanRepayView,
    DepositCreateView,
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
    path('withdrawal/', WithdrawalCreateView.as_view(), name='withdrawal-create'),
]

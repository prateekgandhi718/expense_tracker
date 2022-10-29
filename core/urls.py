from django.urls import path

from core.views import ApprovalRejectionAPIView, ExpenseAPIView, ExpenseDetailAPIView


urlpatterns = [
    path('expense', ExpenseAPIView.as_view(), name = 'expense'),
    path('expense-detail', ExpenseDetailAPIView.as_view(), name = 'expense-detail'),
    path('expense-approval', ApprovalRejectionAPIView.as_view(), name = 'approval-rejection'),
]
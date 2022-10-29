from django.urls import path

from core.views import ExpenseAPIView


urlpatterns = [
    path('expense', ExpenseAPIView.as_view(), name = 'expense')
]
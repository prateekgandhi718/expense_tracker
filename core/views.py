from django.shortcuts import render
from rest_framework.views import APIView

from utils.common import success_response

# Create your views here.
class ExpenseAPIView(APIView):
    def get(self, request):
        pass

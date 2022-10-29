from django.shortcuts import render
from rest_framework.views import APIView
from core.models import Expense
from core.serializers import ExpenseSerializer, ExpenseSerializerWithoutReciept
from utils.azure_file_controller import upload_file_to_blob

from utils.common import bad_request_response, success_response

# Create your views here.
class ExpenseAPIView(APIView):
    def post(self, request):
        if request.data.get('reciept') != "":
            serializer = ExpenseSerializer(data=request.data)

            if serializer.is_valid():
                new_image_name = upload_file_to_blob(request.data.get('reciept')) #this uploads the incoming image to storage account
                request.data.get('reciept').name = new_image_name #this sets the incoming picture name to new name
                Expense(category = request.data.get('category'), date = request.data.get('date'), amount = request.data.get('amount'), comments = request.data.get('comments'), reciept = request.data.get('reciept')).save()
                return success_response(data = [], message="Expense recorded successfully")
                
            else:
                return bad_request_response(data = serializer.errors, message = "Bad request")
        else:
            serializer = ExpenseSerializerWithoutReciept(data = request.data)
            if serializer.is_valid():
                Expense(category = request.data.get('category'), date = request.data.get('date'), amount = request.data.get('amount'), comments = request.data.get('comments')).save()
                return success_response(data = [], message="Expense recorded successfully")
            else:
                return bad_request_response(data = serializer.errors, message = "Bad request")
        

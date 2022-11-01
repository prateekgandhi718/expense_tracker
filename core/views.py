from django.shortcuts import render
from rest_framework.views import APIView
from core.models import Expense
from core.serializers import ExpenseSerializer, ExpenseSerializerWithoutReciept
from utils.azure_file_controller import upload_file_to_blob
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
import json

from utils.common import bad_request_response, not_found_response, success_response
from datetime import date, timedelta

#Initialising queue client.
queue_client = QueueClient.from_connection_string(conn_str='DefaultEndpointsProtocol=https;AccountName=assessmentstgacc;AccountKey=eiyYAT6BkNDxxQ1KSFDEjkJ87GXUvAqO1By/bW1m0WTN0MWp5PSFrDYw0lAfHza17CCpUEYYTNhp+AStufDnyw==;EndpointSuffix=core.windows.net', queue_name="prateek-queue", message_encode_policy = BinaryBase64EncodePolicy(), message_decode_policy = BinaryBase64DecodePolicy())

# Create your views here.
class ExpenseAPIView(APIView):
    def post(self, request):
        if request.data.get('reciept') != "":
            serializer = ExpenseSerializer(data=request.data)

            if serializer.is_valid():
                new_image_name = upload_file_to_blob(request.data.get('reciept')) #this uploads the incoming image to storage account
                request.data.get('reciept').name = new_image_name #this sets the incoming picture name to new name
                Expense(category = request.data.get('category'), date = request.data.get('date'), amount = request.data.get('amount'), comments = request.data.get('comments'), reciept = request.data.get('reciept'), status = 'pending').save()
                #queue sdk and operations.
                latest_obj_id = str(Expense.objects.latest('id').id)
                latest_obj_id_bytes = latest_obj_id.encode('ascii')
                queue_client.send_message(latest_obj_id_bytes)
                return success_response(data = [], message="Expense recorded successfully")
                
            else:
                return bad_request_response(data = serializer.errors, message = "Bad request")
        else:
            serializer = ExpenseSerializerWithoutReciept(data = request.data)
            if serializer.is_valid():
                Expense(category = request.data.get('category'), date = request.data.get('date'), amount = request.data.get('amount'), comments = request.data.get('comments'), status = 'pending').save()
                #queue sdk and operations.
                latest_obj_id = str(Expense.objects.latest('id').id)
                latest_obj_id_bytes = latest_obj_id.encode('ascii')
                queue_client.send_message(latest_obj_id_bytes)
                return success_response(data = [], message="Expense recorded successfully")
            else:
                return bad_request_response(data = serializer.errors, message = "Bad request")
    
    def get(self, request):
        filter = request.GET.get('filter')
        response = {
                'expenses' : []
            }
        if filter == 'approver':
            #get for approvers
            start_date = date.today()
            end_date = start_date + timedelta(days=-30)
            objs = Expense.objects.filter(amount__gte = 500, date__range = [end_date, start_date])
        elif filter == 'pending':
            objs = Expense.objects.filter(status = 'pending')
        elif filter == 'approved':
            objs = Expense.objects.filter(status = 'approved')
        elif filter == 'rejected':
            objs = Expense.objects.filter(status = 'rejected')
        else:
            objs = Expense.objects.all()
        
        if objs:
            for obj in objs:
                response['expenses'].append(
                    {
                        'id' : obj.id,
                        'category' : obj.category,
                        'date' : obj.date,
                        'amount' : obj.amount,
                        'comments' : obj.comments,
                        'reciept' : obj.reciept.url if obj.reciept else None,
                        'status' : obj.status
                    }
                )
            return success_response(data = response['expenses'], message='success')
        else:
            return not_found_response(data = [], message='Not found')
        
class ExpenseDetailAPIView(APIView):
    def get(self, request):
        exp_id = request.GET.get('id')
        try:
            obj = Expense.objects.get(id = exp_id)
            response = {
                'id' : obj.id,
                'category' : obj.category,
                'date' : obj.date,
                'amount' : obj.amount,
                'comments' : obj.comments,
                'reciept' : obj.reciept.url if obj.reciept else None,
                'status' : obj.status
            }
            return success_response(data = response, message = 'Found successfully')
        except:
            return not_found_response(data = [], message='Not found')

class ApprovalRejectionAPIView(APIView):
    def post(self, request):
        exp_id = request.GET.get('id')
        operation = request.GET.get('operation')
        comments = request.data.get('comments')
        try:
            obj = Expense.objects.get(id = exp_id)
            if operation == 'approve':
                Expense.objects.filter(id = exp_id).update(status = 'approved', comments = comments)
            else:
                Expense.objects.filter(id = exp_id).update(status = 'rejected', comments = comments)
            return success_response(data = [], message = f"Expense has been {operation}d successfully")
        except:
            return not_found_response(data = [], message='Not found')
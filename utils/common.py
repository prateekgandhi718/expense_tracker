from rest_framework.response import Response
from rest_framework import status

def success_response(data = None, message = None):
    return Response({
        "status": "success",
        "message": message,
        "data" : data,
    }, status.HTTP_200_OK)

def not_found_response(data = None, message = None):
    return Response({
        "status": "not found",
        "message": message,
        "data" : data,
    }, status.HTTP_404_NOT_FOUND)

def failure_response(data = None, message = None):
    return Response({
        "status": "failure",
        "message": "Internal server error",
        "data" : data,
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)

def bad_request_response(data = None, message = None):
    return Response({
        "status": "bad request",
        "message": message,
        "data" : data,
    }, status.HTTP_400_BAD_REQUEST)

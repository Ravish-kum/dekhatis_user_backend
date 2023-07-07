from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken

def custom_exception_handler(exception, context):
    handlers ={
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
        'InvalidToken': _handle_authentication_error,
        'Exception': _handle_generic_error,  
        'BaseException': _handle_generic_error,
        'Http500': _handle_generic_error
    }

    response = exception_handler(exception, context)
    exception_class =exception.__class__.__name__


    if exception_class in handlers:
        return handlers[exception_class](exception, context, response)
    return response

def _handle_authentication_error(exception, context, response):

    response.data ={
        "error":"please signin to proceed",
        "status_code": 401
    }
    return response

def _handle_generic_error(exception, context, response):
    return response


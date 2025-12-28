from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats errors as:
    {
        "detail": "message",
        "code": "error_code"
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'detail': response.data.get('detail', str(exc)),
            'code': response.data.get('code', exc.__class__.__name__)
        }
        response.data = custom_response_data
    else:
        # Handle unexpected errors
        custom_response_data = {
            'detail': str(exc),
            'code': 'server_error'
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


from django.http import JsonResponse
def error_404(request, exception):
    message ="the endpoint is not found"

    response = JsonResponse(data={'message':message, 'status_code':404})
    response.status_code= 404
    return response

def error_500(request):
    message ="endpoint not found from server side"

    response = JsonResponse(data={'message':message, 'status_code':500})
    response.status_code= 500
    return response
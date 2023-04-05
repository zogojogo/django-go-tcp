from django.views.decorators.csrf import csrf_exempt
from entry_task.utils.response import response_error_json

class GeneralViews:
    def __init__(self):
        pass

    @csrf_exempt
    def endpoint_not_found(self, request):
        return response_error_json("Endpoint not found", 404)
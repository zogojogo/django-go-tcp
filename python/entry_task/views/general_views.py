from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
import json

class GeneralViews:
    def __init__(self):
        pass

    @csrf_exempt
    def endpoint_not_found(self, request):
        response = OrderedDict([
            ("code", 404),
            ("message", "Endpoint not found")
        ])
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)
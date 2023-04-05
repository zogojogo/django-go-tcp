from django.http import HttpResponse
import json
from collections import OrderedDict

def response_success_json(data, status=200):
    response = OrderedDict([
        ("code", status),
        ("data", data)
    ])
    return HttpResponse(json.dumps(response), content_type="application/json", status=status)

def response_error_json(message, status):
    response = OrderedDict([
        ("code", status),
        ("message", message)
    ])
    return HttpResponse(json.dumps(response), content_type="application/json", status=status)

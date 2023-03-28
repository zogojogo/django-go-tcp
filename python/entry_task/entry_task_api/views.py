from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .repositories import ProductRepository
from .usecases import ProductUsecase
from .dtos import ProductSearchDTO

product_repository = ProductRepository()
product_usecase = ProductUsecase(product_repository)

@csrf_exempt
def product_list(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        req = ProductSearchDTO(**body)
        dto_list = product_usecase.list(req)

        response = {
            "code": 200,
            "data": dto_list
        }

        return HttpResponse(json.dumps(response), content_type="application/json", status=200)
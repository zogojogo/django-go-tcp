from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from entry_task.repository.product_repository import ProductRepository
from entry_task.usecase.product_usecase import ProductUsecase
from entry_task.dto.product_dto import ProductSearchDTO
from entry_task.models.products import Product

class ProductViews:
    def __init__(self):
        self.product_repository = ProductRepository(Product)
        self.product_usecase = ProductUsecase(self.product_repository)

    @csrf_exempt
    def product_list(self, request):
        if request.method == 'POST':
            body = json.loads(request.body)
            req = ProductSearchDTO(**body)
            res = self.product_usecase.list(req)

            response = {
                "code": 200,
                "data": res
            }
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)

    @csrf_exempt
    def product_details(self, request, id):
        if request.method == 'GET':
            res = self.product_usecase.details(id)

            response = {
                "code": 200,
                "data": res
            }
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
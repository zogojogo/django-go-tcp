from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
import json
from entry_task.repository.product_repository import ProductRepository
from entry_task.usecase.product_usecase import ProductUsecase
from entry_task.dto.product_dto import ProductSearchDTO
from entry_task.models.app_models import Product
from entry_task.errors.product_errors import ProductNotFoundError, ProductsNotFoundError, PageCursorsSetAtSameTimeError
from entry_task.utils.http_statuses import HTTPStatus

class ProductViews:
    def __init__(self):
        self.product_repository = ProductRepository(Product)
        self.product_usecase = ProductUsecase(self.product_repository)

    @csrf_exempt
    def product_list(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                req = ProductSearchDTO(**body)
                req.validate()
                res = self.product_usecase.list(req)

                response = {
                    "code": HTTPStatus.OK,
                    "data": res
                }
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.OK)
            except PageCursorsSetAtSameTimeError as e:
                response = OrderedDict([
                    ("code", HTTPStatus.BAD_REQUEST),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.BAD_REQUEST)
            except ProductsNotFoundError as e:
                response = OrderedDict([
                    ("code", HTTPStatus.NOT_FOUND),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.NOT_FOUND)
            except Exception as e:
                response = OrderedDict([
                    ("code", HTTPStatus.INTERNAL_SERVER_ERROR),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def product_details(self, request, id):
        if request.method == 'GET':
            try:
                res = self.product_usecase.details(id)
                response = OrderedDict([
                    ("code", HTTPStatus.OK),
                    ("data", res)
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.OK)
            except ProductNotFoundError as e:
                response = OrderedDict([
                    ("code", HTTPStatus.NOT_FOUND),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.NOT_FOUND)
            except Exception as e:
                response = OrderedDict([
                    ("code", HTTPStatus.INTERNAL_SERVER_ERROR),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.INTERNAL_SERVER_ERROR)
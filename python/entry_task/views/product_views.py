import json
from django.views.decorators.csrf import csrf_exempt
from entry_task.repository.product_repository import ProductRepository
from entry_task.usecase.product_usecase import ProductUsecase
from entry_task.dto.product_dto import ProductSearchDTO
from entry_task.models.app_models import Product
from entry_task.errors.product_errors import ProductNotFoundError, ProductsNotFoundError, PageCursorsSetAtSameTimeError, LimitOutOfRangeError, CursorNegativeError
from entry_task.errors.general_errors import InternalServerError
from entry_task.utils.http_statuses import HTTPStatus
from entry_task.utils.response import response_error_json, response_success_json
import time

class ProductViews:
    def __init__(self):
        self.product_repository = ProductRepository(Product)
        self.product_usecase = ProductUsecase(self.product_repository)

    @csrf_exempt
    def product_list(self, request):
        if request.method == 'GET':
            try:
                q = request.GET.get('q')
                prev_cursor = request.GET.get('prev_cursor')
                next_cursor = request.GET.get('next_cursor')
                limit = request.GET.get('limit')
                cat = request.GET.get('cat')

                prev_cursor_int = int(prev_cursor) if prev_cursor else None
                next_cursor_int = int(next_cursor) if next_cursor else None
                limit_int = int(limit) if limit else None
                cat_int = int(cat) if cat else None
                req = ProductSearchDTO(q=q, prev_cursor=prev_cursor_int, next_cursor=next_cursor_int, limit=limit_int, cat=cat_int)
                req.validate()
                res = self.product_usecase.list(req)

                return response_success_json(res)
            except (PageCursorsSetAtSameTimeError, CursorNegativeError, LimitOutOfRangeError) as e:
                return response_error_json(str(e), HTTPStatus.BAD_REQUEST)
            except ProductsNotFoundError as e:
                return response_error_json(str(e), HTTPStatus.NOT_FOUND)
            except Exception as e:
                return response_error_json(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def product_details(self, request, id):
        if request.method == 'GET':
            try:
                res = self.product_usecase.details(id)
                return response_success_json(res)
            except ProductNotFoundError as e:
                return response_error_json(str(e), HTTPStatus.NOT_FOUND)
            except Exception as e:
                return response_error_json("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)
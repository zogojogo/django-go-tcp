from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from entry_task.repository.product_comment_repository import ProductCommentRepository
from entry_task.usecase.product_comment_usecase import ProductCommentUsecase
from entry_task.models.app_models import ProductComment
from entry_task.errors.product_comment_errors import CommentsNotFoundError, ParentIDNegativeError, CursorNegativeError, LimitOutOfRangeError
from entry_task.dto.product_comment_dto import ProductCommentQueryParamDTO
from entry_task.utils.http_statuses import HTTPStatus

class ProductCommentViews:
    def __init__(self):
        self.product_comment_repository = ProductCommentRepository(ProductComment)
        self.product_comment_usecase = ProductCommentUsecase(self.product_comment_repository)

    @csrf_exempt
    def product_comment_list(self, request, id):
        if request.method == 'GET':
            try:
                cursor = request.GET.get('cursor')
                limit = request.GET.get('limit')
                parent_comment_id = request.GET.get('parent_comment_id')

                cursor_int = int(cursor) if cursor else None
                limit_int = int(limit) if limit else None
                parent_comment_id_int = int(parent_comment_id) if parent_comment_id else None
                req = ProductCommentQueryParamDTO(parent_id=parent_comment_id_int, cursor=cursor_int, limit=limit_int)
                req.validate()
                res = self.product_comment_usecase.list(id, req)
                response = {
                    "code": HTTPStatus.OK,
                    "data": res
                }
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.OK)
            except CommentsNotFoundError as e:
                response = {
                    "code": HTTPStatus.NOT_FOUND,
                    "message": str(e)
                }
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.NOT_FOUND)
            except (CursorNegativeError, ParentIDNegativeError, LimitOutOfRangeError) as e:
                response = {
                    "code": HTTPStatus.BAD_REQUEST,
                    "message": str(e)
                }
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.BAD_REQUEST)
            except Exception as e:
                response = {
                    "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message": str(e)
                }
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.INTERNAL_SERVER_ERROR)
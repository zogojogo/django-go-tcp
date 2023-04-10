from django.views.decorators.csrf import csrf_exempt
import json
from entry_task.repository.product_comment_repository import ProductCommentRepository
from entry_task.usecase.product_comment_usecase import ProductCommentUsecase
from entry_task.models.app_models import ProductComment
from entry_task.errors.product_comment_errors import CommentsNotFoundError, ParentIDNegativeError, CursorNegativeError, LimitOutOfRangeError, CommentTextTooLongError, CommentTextRequiredError, ProductIDRequiredError, UserIDRequiredError, ProductConstraintError
from entry_task.errors.general_errors import InternalServerError
from entry_task.dto.product_comment_dto import ProductCommentQueryParamDTO, AddProductCommentDTO
from entry_task.utils.http_statuses import HTTPStatus
from entry_task.utils.response import response_error_json, response_success_json

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
                return response_success_json(res)
            except CommentsNotFoundError as e:
                return response_error_json(str(e), HTTPStatus.NOT_FOUND)
            except (CursorNegativeError, ParentIDNegativeError, LimitOutOfRangeError) as e:
                return response_error_json(str(e), HTTPStatus.BAD_REQUEST)
            except Exception as e:
                return response_error_json("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)
        
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                user = request.user
                dto = AddProductCommentDTO(
                    comment_text=body['comment_text'],
                    parent_comment_id=body['parent_comment_id'],
                    user_id=user.get('user_id'),
                    product_id=id
                )
                dto.validate()
                res = self.product_comment_usecase.add(dto)
                return response_success_json(res, HTTPStatus.CREATED)
            
            except (CommentTextTooLongError, CommentTextRequiredError, ProductIDRequiredError, UserIDRequiredError, ProductConstraintError) as e:
                return response_error_json(str(e), HTTPStatus.BAD_REQUEST)

            except Exception as e:
                return response_error_json("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)
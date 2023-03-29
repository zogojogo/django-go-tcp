from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from entry_task.repository.product_comment_repository import ProductCommentRepository
from entry_task.usecase.product_comment_usecase import ProductCommentUsecase
from entry_task.models.products import ProductComment

class ProductCommentViews:
    def __init__(self):
        self.product_comment_repository = ProductCommentRepository(ProductComment)
        self.product_comment_usecase = ProductCommentUsecase(self.product_comment_repository)

    @csrf_exempt
    def product_comment_list(self, request, id):
        if request.method == 'GET':
            res = self.product_comment_usecase.list(id)

            response = {
                "code": 200,
                "data": res
            }
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
from django.core.exceptions import ObjectDoesNotExist
from entry_task.errors.product_comment_errors import CommentsNotFoundError, ProductConstraintError
from entry_task.errors.general_errors import InternalServerError
from django.db import IntegrityError

class ProductCommentRepository:
    def __init__(self, product_comment_model):
        self.product_comment_model = product_comment_model

    def get_by_product_id(self, id, req):
        try:
            if req.parent_id != 0:
                base_query = self.product_comment_model.objects.filter(product_id=id, parent_comment=req.parent_id)
            else:
                base_query = self.product_comment_model.objects.filter(product_id=id).filter(parent_comment__isnull=True)

            if len(base_query) == 0:
                return [], 0
            
            if req.cursor:
                base_query = base_query.filter(id__gt=req.cursor)
            
            comments = base_query.all()[:req.limit+1]
            cursor = comments[len(comments)-2].id if len(comments) > req.limit else 0
            return comments[:req.limit], cursor
            
        except ObjectDoesNotExist as e:
            raise CommentsNotFoundError()
        
        except Exception as e:
            raise InternalServerError(str(e))
        
    def check_comment_has_child(self, id):
        try:
            return self.product_comment_model.objects.filter(parent_comment=id).exists()
        
        except Exception as e:
            raise InternalServerError(str(e))
        
    def add_new_comment(self, comment):
        try:
            return self.product_comment_model.objects.create(**comment)
        
        except IntegrityError as e:
            code = e[0]
            CONSTRAIN_ERR = 1452
            if code == CONSTRAIN_ERR:
                raise ProductConstraintError()
            raise InternalServerError("An error occured while adding new comment")

        except Exception as e:
            raise InternalServerError(str(e))    
    
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

class ProductCommentRepository:
    def __init__(self, product_comment_model):
        self.product_model = product_comment_model

    def get_by_product_id(self, id, parent_id):
        try:
            if parent_id != 0:
                return self.product_model.objects.filter(product_id=id, parent_comment=parent_id).all()
            else:
                return self.product_model.objects.filter(product_id=id).filter(parent_comment__isnull=True).all()
            
        except ObjectDoesNotExist as e:
            error_msg = 'Product not found: {}'.format(str(e))
            return HttpResponse(error_msg, status=404)
        
        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
            return HttpResponse(error_msg, status=500)
        
    def check_comment_has_child(self, id):
        try:
            return self.product_model.objects.filter(parent_comment=id).exists()
            
        except ObjectDoesNotExist as e:
            error_msg = 'Product not found: {}'.format(str(e))
            return HttpResponse(error_msg, status=404)
        
        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
            return HttpResponse(error_msg, status=500)
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from entry_task.errors.product_errors import ProductNotFoundError, ProductsNotFoundError
from entry_task.errors.general_errors import InternalServerError
from django.db.models import Q

class ProductRepository:
    def __init__(self, product_model):
        self.product_model = product_model

    def get_all(self, req):    
        try:
            if req.prev_cursor != 0:
                prods = self.product_model.objects.select_related('productcategory').filter(
                    Q(title__icontains=req.q) if req.q != '' else Q(),
                    Q(id__lt=req.prev_cursor),
                    Q(productcategory__category_id=req.cat) if req.cat != 0 else Q()
                ).order_by('-id')[:req.limit+1][::-1]
                next_cursor = prods[len(prods)-1].id if len(prods) > 0 else 0
                prev_cursor = prods[0].id if len(prods) > req.limit else 0
                return prods[1:req.limit+1] if len(prods) > req.limit else prods[:req.limit], prev_cursor, next_cursor
            
            else:
                prods = self.product_model.objects.select_related('productcategory').filter(
                    Q(title__icontains=req.q) if req.q != '' else Q(),
                    Q(id__gt=req.next_cursor),
                    Q(productcategory__category_id=req.cat) if req.cat != 0 else Q()
                )[:req.limit+1]
            
            if not prods.exists():
                return [],0,0

            next_cursor = prods[len(prods)-2].id if len(prods) > req.limit else 0
            prev_cursor = prods[0].id if len(prods) > 0 else 0
            return prods[:req.limit], prev_cursor, next_cursor
    
        except ObjectDoesNotExist as e:
            raise ProductsNotFoundError()

        except Exception as e:
            raise InternalServerError(str(e))
        
    def get_details(self, id):
        try:
            prod = self.product_model.objects.select_related('productcategory').get(id=id)
            return prod

        except ObjectDoesNotExist as e:
            raise ProductNotFoundError()
        
        except Exception as e:
            raise InternalServerError(str(e))
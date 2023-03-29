from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

class ProductRepository:
    def __init__(self, product_model):
        self.product_model = product_model

    def get_all(self, req):    
        try:
            if req.cat == 0 and req.q == '':
                return [],0,0
            
            base_query = self.product_model.objects.select_related('productcategory').filter(title__icontains=req.q)
            if req.cat != 0:
                base_query = base_query.filter(productcategory__category_id=req.cat)

            if len(base_query) == 0:
                return [],0,0
            
            if req.prev_cursor != 0:
                base_query = base_query.filter(id__lt=req.prev_cursor).order_by('-id')
            elif req.next_cursor != 0:
                base_query = base_query.filter(id__gt=req.next_cursor)

            prods = base_query.all()[:req.limit+1]
            next_cursor = prods[len(prods)-2].id if len(prods) > req.limit else 0
            prev_cursor = 0

            return prods[:req.limit], prev_cursor, next_cursor
    
        except ObjectDoesNotExist as e:
            error_msg = 'Products not found: {}'.format(str(e))
            return HttpResponse(error_msg, status=404)

        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
            return HttpResponse(error_msg, status=500)
        
    def get_details(self, id):
        try:
            prod = self.product_model.objects.select_related('productcategory').get(id=id)
            return prod

        except ObjectDoesNotExist as e:
            error_msg = 'Product not found: {}'.format(str(e))
            return HttpResponse(error_msg, status=404)

        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
            return HttpResponse(error_msg, status=500)
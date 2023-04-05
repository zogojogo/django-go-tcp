from entry_task.dto.product_dto import ProductDTO, ProductListDTO, ProductDetailsDTO, ProductDetailsCategoryDTO
from entry_task.errors.product_errors import ProductNotFoundError, ProductsNotFoundError

class ProductUsecase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def list(self, req):
        try:
            products, prev_cursor, next_cursor = self.product_repository.get_all(req)
        except ProductsNotFoundError as e:
            print('An error occured: {}'.format(e))
            raise e
        
        product_dtos = []
        for product in products:
            if len(product.images.all()) > 0:
                thumbnail_img = product.images.all()[0].image_url
            thumbnail_img = ''
            product_dtos.append(ProductDTO(product, thumbnail_img))
        dto_list = [dto.as_dict() for dto in product_dtos]
        product_list_dto = ProductListDTO(dto_list, prev_cursor, next_cursor).as_dict()
        return product_list_dto
    
    def details(self, id):
        try:
            product = self.product_repository.get_details(id)
        except ProductNotFoundError as e:
            print('An error occured: {}'.format(e))
            raise e

        if product.images.all() is None:
            image_urls = []
        if product.productcategory_set.all() is None:
            categories = []

        image_urls = [image.image_url for image in product.images.all()]
        categories = [ProductDetailsCategoryDTO(productcategory.category).as_dict() for productcategory in product.productcategory_set.all()]
        product_details_dto = ProductDetailsDTO(product, image_urls, categories).as_dict()
        return product_details_dto
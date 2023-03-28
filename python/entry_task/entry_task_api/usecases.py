from .dtos import ProductDTO, ProductListDTO

class ProductUsecase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def list(self, req):
        products, prev_cursor, next_cursor = self.product_repository.get_all(req)
        product_dtos = []
        for product in products:
            image_urls = [image.image_url for image in product.images.all()]
            category_ids = [productcategory.category_id for productcategory in product.productcategory_set.all()]
            product_dtos.append(ProductDTO(product, image_urls, category_ids))
        dto_list = [dto.as_dict() for dto in product_dtos]
        product_list_dto = ProductListDTO(dto_list, prev_cursor, next_cursor).as_dict()
        return product_list_dto
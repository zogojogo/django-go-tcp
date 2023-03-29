from entry_task.dto.product_dto import ProductDTO, ProductListDTO, ProductDetailsDTO, ProductDetailsCategoryDTO

class ProductUsecase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def list(self, req):
        products, prev_cursor, next_cursor = self.product_repository.get_all(req)
        product_dtos = []
        for product in products:
            thumbnail_img = product.images.all()[0].image_url
            # validate index 0 image
            product_dtos.append(ProductDTO(product, thumbnail_img))
        dto_list = [dto.as_dict() for dto in product_dtos]
        product_list_dto = ProductListDTO(dto_list, prev_cursor, next_cursor).as_dict()
        return product_list_dto
    
    def details(self, id):
        product = self.product_repository.get_details(id)
        # handle errornya
        image_urls = [image.image_url for image in product.images.all()]
        # validate product.images .productcategory dll
        categories = [ProductDetailsCategoryDTO(productcategory.category).as_dict() for productcategory in product.productcategory_set.all()]
        product_details_dto = ProductDetailsDTO(product, image_urls, categories).as_dict()
        return product_details_dto
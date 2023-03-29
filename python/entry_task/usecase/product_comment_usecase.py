from entry_task.dto.product_comment_dto import ProductCommentDTO, ProductCommentListDTO, ProductCommentUserDTO

class ProductCommentUsecase:
    def __init__(self, product_comment_repository):
        self.product_comment_repository = product_comment_repository

    def list(self, id):
        product_comments = self.product_comment_repository.get_by_product_id(id, 0)
        product_comment_dtos = []
        for product_comment in product_comments:
            has_child = self.product_comment_repository.check_comment_has_child(id)
            print(has_child)
            user = ProductCommentUserDTO(product_comment.user).as_dict()
            product_comment_dtos.append(ProductCommentDTO(product_comment, user, has_child))
        dto_list = [dto.as_dict() for dto in product_comment_dtos]
        product_comment_list_dto = ProductCommentListDTO(dto_list, 0).as_dict()
        print(product_comment_list_dto)
        return product_comment_list_dto
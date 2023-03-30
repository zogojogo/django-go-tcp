from entry_task.dto.product_comment_dto import ProductCommentDTO, ProductCommentListDTO, ProductCommentUserDTO
from entry_task.errors.product_comment_errors import CommentsNotFoundError
import traceback

class ProductCommentUsecase:
    def __init__(self, product_comment_repository):
        self.product_comment_repository = product_comment_repository

    def list(self, id, req):
        try:
            product_comments, cursor = self.product_comment_repository.get_by_product_id(id, req)
        except CommentsNotFoundError as e:
            print('An error occured: {}'.format(e))
            raise e
        product_comment_dtos = []
        for product_comment in product_comments:
            try:
                has_child = self.product_comment_repository.check_comment_has_child(product_comment.id)
            except Exception as e:
                print('An error occured: {}'.format(e))
                raise e 
            if not product_comment.user:
                user = {}
            user = ProductCommentUserDTO(product_comment.user).as_dict()
            product_comment_dtos.append(ProductCommentDTO(product_comment, user, has_child))
        dto_list = [dto.as_dict() for dto in product_comment_dtos]
        product_comment_list_dto = ProductCommentListDTO(dto_list, cursor).as_dict()
        return product_comment_list_dto
    
    def add(self, req_dto):
        try:
            product_comment = self.product_comment_repository.add_new_comment(req_dto.__dict__)
        except Exception as e:
            print('An error occured: {}'.format(e))
            raise e
        if not product_comment.user:
                user = {}
        user = ProductCommentUserDTO(product_comment.user).as_dict()
        product_comment_dto = ProductCommentDTO(product_comment, user, False).as_dict()
        return product_comment_dto
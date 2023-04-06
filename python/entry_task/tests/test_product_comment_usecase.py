import unittest
from mock import Mock
from entry_task.usecase.product_comment_usecase import ProductCommentUsecase
from entry_task.models.app_models import ProductComment, User
from entry_task.dto.product_comment_dto import ProductCommentDTO, ProductCommentListDTO, ProductCommentUserDTO
from entry_task.errors.product_comment_errors import CommentsNotFoundError, CommentTextRequiredError, CommentTextTooLongError, CursorNegativeError, LimitOutOfRangeError, ParentIDNegativeError, ProductConstraintError, ProductIDRequiredError, UserIDRequiredError
from entry_task.errors.general_errors import InternalServerError

class TestProductCommentListUsecase(unittest.TestCase):
    def test_list_error_comments_not_found(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10}
        product_comment_repository = Mock()
        product_comment_repository.get_by_product_id.side_effect = CommentsNotFoundError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(CommentsNotFoundError):
            usecase.list(product_id, req)

    def test_list_error_cursor_negative(self):
        product_id = 1
        req = {"cursor": -1, "limit": 10}
        product_comment_repository = Mock()
        product_comment_repository.get_by_product_id.side_effect = CursorNegativeError()

        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(CursorNegativeError):
            usecase.list(product_id, req)

    def test_list_error_limit_out_of_range(self):
        product_id = 1
        req = {"cursor": 0, "limit": 11000000000}
        product_comment_repository = Mock()
        product_comment_repository.get_by_product_id.side_effect = LimitOutOfRangeError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(LimitOutOfRangeError):
            usecase.list(product_id, req)

    def test_list_error_parent_id_negative(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10, "parent_comment_id": -1}
        product_comment_repository = Mock()
        product_comment_repository.get_by_product_id.side_effect = ParentIDNegativeError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(ParentIDNegativeError):
            usecase.list(product_id, req)

    def test_list_error_check_child(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10, "parent_comment_id": 1}
        product_comment = Mock(
            has_child=Mock(),
            user=None
        )
        product_comment_repository = Mock()

        product_comment_repository.get_by_product_id.return_value = ([product_comment], 0)
        product_comment_repository.check_comment_has_child.side_effect = InternalServerError()
        usecase = ProductCommentUsecase(product_comment_repository)

        with self.assertRaises(InternalServerError):
            usecase.list(product_id, req)

    def test_list_success(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10}
        product_comment_repository = Mock()
        product_comment_repository.get_by_product_id.return_value = ([], 0)
        usecase = ProductCommentUsecase(product_comment_repository)
        res = usecase.list(product_id, req)

        expected_result = ProductCommentListDTO([], 0).as_dict()
        self.assertEqual(res, expected_result)

    def test_list_success_child(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10, "parent_comment_id": 1}
        product_comment = Mock(
            has_child=Mock(),
            user=None
        )
        product_comment_repository = Mock()
        expected_result = ProductCommentListDTO([
            ProductCommentDTO(
                product_comment, {}, True
            ).as_dict()
        ], 0).as_dict()

        product_comment_repository.get_by_product_id.return_value = ([product_comment], 0)
        product_comment_repository.check_comment_has_child.return_value = True
        usecase = ProductCommentUsecase(product_comment_repository)
        res = usecase.list(product_id, req)

        self.assertEqual(res, expected_result)

    def test_list_success_user(self):
        product_id = 1
        req = {"cursor": 0, "limit": 10}
        product_comment = Mock(
            has_child=Mock(),
            user=Mock(
                id=1,
                username="test",
            )
        )
        product_comment_repository = Mock()
        expected_result = ProductCommentListDTO([
            ProductCommentDTO(product_comment, ProductCommentUserDTO(
                product_comment.user
            ).as_dict(), False).as_dict()
        ], 0).as_dict()

        product_comment_repository.get_by_product_id.return_value = ([product_comment], 0)
        product_comment_repository.check_comment_has_child.return_value = False
        usecase = ProductCommentUsecase(product_comment_repository)
        res = usecase.list(product_id, req)

        self.assertEqual(res, expected_result)


class TestProductCommentAddUsecase(unittest.TestCase):
    def test_add_error_comment_text_required(self):
        product_id = 1
        req = {"user_id": 1, "parent_comment_id": 1, "comment_text": "", "product_id": product_id}
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.side_effect = CommentTextRequiredError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(CommentTextRequiredError):
            usecase.add(req)

    def test_add_error_comment_text_too_long(self):
        product_id = 1
        req = {"user_id": 1, "parent_comment_id": 1, "comment_text": "a" * 1001, "product_id": product_id}
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.side_effect = CommentTextTooLongError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(CommentTextTooLongError):
            usecase.add(req)

    def test_add_error_parent_id_negative(self):
        product_id = 1
        req = {"user_id": 1, "parent_comment_id": -1, "comment_text": "a", "product_id": product_id}
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.side_effect = ParentIDNegativeError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(ParentIDNegativeError):
            usecase.add(req)

    def test_add_error_product_constraint(self):
        product_id = 1
        req = {"user_id": 1, "parent_comment_id": 1, "comment_text": "a", "product_id": product_id}
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.side_effect = ProductConstraintError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(ProductConstraintError):
            usecase.add(req)

    def test_add_error_product_id_required(self):
        product_id = None
        req = {"user_id": 1, "parent_comment_id": 1, "comment_text": "a", "product_id": product_id}
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.side_effect = ProductIDRequiredError()
        usecase = ProductCommentUsecase(product_comment_repository)
        with self.assertRaises(ProductIDRequiredError):
            usecase.add(req)

    def test_add_success(self):
        product_id = 1
        req = {"user_id": 1, "parent_comment_id": 1, "comment_text": "a", "product_id": product_id}
        user = User(id=1, username="zogojogo")
        comment = ProductComment(user=user, parent_comment_id=1, comment_text="a")
        product_comment_repository = Mock()
        product_comment_repository.add_new_comment.return_value = comment
        usecase = ProductCommentUsecase(product_comment_repository)
        res = usecase.add(req)

        expected_user = ProductCommentUserDTO(user).as_dict()
        expected_result = ProductCommentDTO(comment, expected_user, False).as_dict()
        self.assertEqual(res, expected_result)
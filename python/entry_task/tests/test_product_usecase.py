import unittest
from mock import Mock
from entry_task.dto.product_dto import ProductListDTO, ProductDetailsDTO
from entry_task.errors.product_errors import ProductsNotFoundError, ProductNotFoundError
from entry_task.usecase.product_usecase import ProductUsecase


class TestProductUsecaseList(unittest.TestCase):
    def test_list(self):
        req = Mock()
        product_repository = Mock()
        product_repository.get_all.return_value = ([], 0, 10)
        usecase = ProductUsecase(product_repository)

        result = usecase.list(req)

        expected_result = ProductListDTO([], 0, 10).as_dict()
        self.assertEqual(result, expected_result)

    def test_list_product_image_empty(self):
        req = Mock()
        product_repository = Mock()
        product_repository.get_all.return_value = ([], 0, 10)
        product_repository.images.all.return_value = []
        usecase = ProductUsecase(product_repository)

        result = usecase.list(req)

        expected_result = ProductListDTO([], 0, 10).as_dict()
        self.assertEqual(result, expected_result)


    def test_list_error(self):
        req = {} 
        product_repository = Mock()
        product_repository.get_all.side_effect = ProductsNotFoundError()
        usecase = ProductUsecase(product_repository)

        with self.assertRaises(ProductsNotFoundError):
            usecase.list(req)



    def test_detail_error(self):
        id = 1  
        product_repository = Mock()
        product_repository.get_details.side_effect = ProductNotFoundError()
        usecase = ProductUsecase(product_repository)

        with self.assertRaises(ProductNotFoundError):
            usecase.details(id)

    def test_detail_success(self):
        id = 1
        product_repository = Mock()
        product = Mock()
        product_repository.get_details.return_value = product
        product.images.all.return_value = []
        product.productcategory_set.all.return_value = []
        usecase = ProductUsecase(product_repository)

        result = usecase.details(id)

        expected_result = ProductDetailsDTO(product, [], []).as_dict()
        self.assertEqual(result, expected_result)
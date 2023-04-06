import unittest
from mock import Mock
from entry_task.dto.product_dto import ProductListDTO, ProductDetailsDTO, ProductDTO, ProductDetailsCategoryDTO
from entry_task.errors.product_errors import ProductsNotFoundError, ProductNotFoundError
from entry_task.usecase.product_usecase import ProductUsecase
from collections import OrderedDict

class TestProductUsecaseList(unittest.TestCase):
    def test_list(self):
        req = Mock()
        product_repository = Mock()
        product_repository.get_all.return_value = ([], 0, 10)
        product_repository.images.all.return_value = []
        usecase = ProductUsecase(product_repository)

        result = usecase.list(req)

        expected_result = ProductListDTO([], 0, 10).as_dict()
        self.assertEqual(result, expected_result)

    def test_list_with_images(self):
        req = Mock()

        product_repository = Mock()
        product1 = Mock()
        product1.id = 1
        product1.name = "Product 1"
        product1.description = "Description 1"
        product1.images.all.return_value = [Mock(image_url="https://example.com/image1.jpg")]
        product2 = Mock()
        product2.id = 2
        product2.name = "Product 2"
        product2.description = "Description 2"
        product2.images.all.return_value = [Mock(image_url="https://example.com/image2.jpg")]
        product_repository.get_all.return_value = ([product1, product2], 0, 10)

        usecase = ProductUsecase(product_repository)

        result = usecase.list(req)
        expected_result = ProductListDTO(
            next_cursor=10,
            prev_cursor=0,
            products=[
                ProductDTO(
                    product=product1,
                    image_url="https://example.com/image1.jpg"
                ).as_dict(),
                ProductDTO(
                    product=product2,
                    image_url="https://example.com/image2.jpg"
                ).as_dict(),
            ]
        ).as_dict()
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

    def test_detail_with_images(self):
        product_repository = Mock()
        product = Mock()
        product.id = 1
        product.name = "Product 1"
        product.description = "Description 1"
        product.images.all.return_value = [Mock(image_url="https://example.com/image1.jpg")]

        product_repository.get_details.return_value = product
        product.productcategory_set.all.return_value = []
        usecase = ProductUsecase(product_repository)

        result = usecase.details(1)

        expected_result = ProductDetailsDTO(
            product=product,
            image_urls=["https://example.com/image1.jpg"],
            categories=[]
        ).as_dict()

        self.assertEqual(result, expected_result)

    def test_detail_with_categories(self):
        product_repository = Mock()
        product = Mock()
        product.id = 1
        product.name = "Product 1"
        product.description = "Description 1"
        product.images.all.return_value = []

        productcategory1 = Mock(
            category=Mock(
                id=1,
                name="Category 1",
            ),
        )
        productcategory2 = Mock(
            category=Mock(
                id=2,
                name="Category 2",
            ),
        )
        product.productcategory_set.all.return_value = [productcategory1, productcategory2]

        product_repository.get_details.return_value = product
        usecase = ProductUsecase(product_repository)

        result = usecase.details(1)

        expected_result = ProductDetailsDTO(
            product=product,
            image_urls=[],
            categories=[
                ProductDetailsCategoryDTO(productcategory1.category).as_dict(),
                ProductDetailsCategoryDTO(productcategory2.category).as_dict()
            ]
        ).as_dict()
        print(expected_result)

        self.assertEqual(result, expected_result)

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
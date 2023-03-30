from collections import OrderedDict
from entry_task.errors.product_errors import PageCursorsSetAtSameTimeError

class ProductDetailsDTO:
    def __init__(self, product, image_urls, categories):
        self.id = product.id
        self.title = product.title
        self.description = product.description
        self.images = image_urls
        self.categories = categories

    def as_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('description', self.description),
            ('categories', self.categories),
            ('images', self.images),
        ])
    
class ProductDetailsCategoryDTO:
    def __init__(self, category):
        self.id = category.id
        self.name = category.name

    def as_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('name', self.name),
        ])
    
class ProductDTO:
    def __init__(self, product, image_url):
        self.id = product.id
        self.title = product.title
        self.thumbnail_img = image_url

    def as_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('thumbnail_img', self.thumbnail_img)
        ])

    
class ProductListDTO:
    def __init__(self, products, prev_cursor, next_cursor):
        self.products = products
        self.prev_cursor = prev_cursor
        self.next_cursor = next_cursor

    def as_dict(self):
        return OrderedDict([
            ('prev_cursor', self.prev_cursor),
            ('next_cursor', self.next_cursor),
            ('products', self.products),
        ])

class ProductSearchDTO:
    def __init__(self, next_cursor, prev_cursor, q='', cat=0, limit=10):
        self.q = q
        self.cat = cat
        self.limit = limit
        self.next_cursor = next_cursor
        self.prev_cursor = prev_cursor
    
    def validate(self):
        if self.next_cursor and self.prev_cursor:
            print('An error occured: {}'.format(PageCursorsSetAtSameTimeError()))
            raise PageCursorsSetAtSameTimeError()

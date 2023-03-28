from collections import OrderedDict

class ProductDTO:
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
    def __init__(self, q='', cat=0, limit=10, next_cursor=0, prev_cursor=0):
        self.q = q
        self.cat = cat
        self.limit = limit
        self.next_cursor = next_cursor
        self.prev_cursor = prev_cursor
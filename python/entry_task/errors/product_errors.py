class ProductNotFoundError(Exception):
    def __init__(self, message='Product not found'):
        super(ProductNotFoundError, self).__init__(message)
    
class ProductsNotFoundError(Exception):
    def __init__(self, message='Products not found'):
        super(ProductsNotFoundError, self).__init__(message)

class PageCursorsSetAtSameTimeError(Exception):
    def __init__(self, message='Page cursors cannot be set at the same time'):
        super(PageCursorsSetAtSameTimeError, self).__init__(message)

class LimitOutOfRangeError(Exception):
    def __init__(self, message='Limit must be between 1 and 100'):
        super(LimitOutOfRangeError, self).__init__(message)

class CursorNegativeError(Exception):
    def __init__(self, message='Cursor must be greater than 0'):
        super(CursorNegativeError, self).__init__(message)
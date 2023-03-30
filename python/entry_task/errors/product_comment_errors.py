class CommentsNotFoundError(Exception):
    def __init__(self, message='Comments not found'):
        super(CommentsNotFoundError, self).__init__(message)

class LimitOutOfRangeError(Exception):
    def __init__(self, message='Limit must be between 1 and 100'):
        super(LimitOutOfRangeError, self).__init__(message)

class CursorNegativeError(Exception):
    def __init__(self, message='Cursor must be greater than 0'):
        super(CursorNegativeError, self).__init__(message)

class ParentIDNegativeError(Exception):
    def __init__(self, message='Parent ID must be greater than 0'):
        super(ParentIDNegativeError, self).__init__(message)

class CommentTextRequiredError(Exception):
    def __init__(self, message='Comment text is required'):
        super(CommentTextRequiredError, self).__init__(message)

class ProductIDRequiredError(Exception):
    def __init__(self, message='Product ID is required'):
        super(ProductIDRequiredError, self).__init__(message)

class UserIDRequiredError(Exception):
    def __init__(self, message='User ID is required'):
        super(UserIDRequiredError, self).__init__(message)

class CommentTextTooLongError(Exception):
    def __init__(self, message='Comment text is too long'):
        super(CommentTextTooLongError, self).__init__(message)
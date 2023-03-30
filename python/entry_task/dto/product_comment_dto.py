from collections import OrderedDict
from entry_task.errors.product_comment_errors import CursorNegativeError, LimitOutOfRangeError, ParentIDNegativeError, CommentTextRequiredError, ProductIDRequiredError, UserIDRequiredError, CommentTextTooLongError

class ProductCommentQueryParamDTO:
    def __init__(self, parent_id=0, limit=10, cursor=0):
        self.parent_id = parent_id
        self.limit = limit
        self.cursor = cursor

    def validate(self):
        if self.limit < 1 or self.limit > 100:
            print('An error occured: {}'.format(LimitOutOfRangeError()))
            raise LimitOutOfRangeError()

        if self.cursor < 0:
            print('An error occured: {}'.format(CursorNegativeError()))
            raise CursorNegativeError()
        
        if self.parent_id < 0:
            print('An error occured: {}'.format(ParentIDNegativeError()))
            raise ParentIDNegativeError()

class ProductCommentDTO:
    def __init__(self, comment, user, has_reply):
        self.id = comment.id
        self.comment_text = comment.comment_text
        self.user = user
        self.has_reply = has_reply

    def as_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('user', self.user),
            ('comment_text', self.comment_text),
            ('has_reply', self.has_reply),
        ])
    
class ProductCommentUserDTO:
    def __init__(self, user):
        self.id = user.id
        self.username = user.username

    def as_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('username', self.username),
        ])
    
class ProductCommentListDTO:
    def __init__(self, comments, cursor):
        self.comments = comments
        self.cursor = cursor

    def as_dict(self):
        return OrderedDict([
            ('cursor', self.cursor),
            ('comments', self.comments),
        ])
    
class AddProductCommentDTO:
    def __init__(self, comment_text, product_id, user_id, parent_comment_id):
        self.comment_text = comment_text
        self.product_id = product_id
        self.user_id = user_id
        self.parent_comment_id = parent_comment_id

    def validate(self):
        if self.comment_text is None or self.comment_text == '':
            raise CommentTextRequiredError()
        if self.product_id is None or self.product_id == 0:
            raise ProductIDRequiredError()
        if self.user_id is None or self.user_id == 0:
            raise UserIDRequiredError()
        if len(self.comment_text) > 255:
            raise CommentTextTooLongError()
        if self.parent_comment_id == 0:
            self.parent_comment_id = None

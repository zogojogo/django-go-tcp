from collections import OrderedDict

class ProductCommentQueryParamDTO:
    def __init__(self, parent_id=0, limit=10, cursor=0):
        self.parent_id = parent_id
        self.limit = limit
        self.cursor = cursor

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

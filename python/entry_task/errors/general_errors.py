class InternalServerError(Exception):
    def __init__(self, message='Internal server error'):
        super(InternalServerError, self).__init__(message)
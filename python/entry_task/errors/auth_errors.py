class UsernameRequiredError(Exception):
    def __init__(self, message='Username is required'):
        super(UsernameRequiredError, self).__init__(message)

class PasswordRequiredError(Exception):
    def __init__(self, message='Password is required'):
        super(PasswordRequiredError, self).__init__(message)

class EmailRequiredError(Exception):
    def __init__(self, message='Email is required'):
        super(EmailRequiredError, self).__init__(message)

class UsernameTooLongError(Exception):
    def __init__(self, message='Username is too long'):
        super(UsernameTooLongError, self).__init__(message)

class PasswordTooLongError(Exception):
    def __init__(self, message='Password is too long'):
        super(PasswordTooLongError, self).__init__(message)

class EmailTooLongError(Exception):
    def __init__(self, message='Email is too long'):
        super(EmailTooLongError, self).__init__(message)

class InvalidEmailError(Exception):
    def __init__(self, message='Invalid email format'):
        super(InvalidEmailError, self).__init__(message)
from collections import OrderedDict
from entry_task.errors.auth_errors import UsernameRequiredError, PasswordRequiredError, EmailRequiredError, UsernameTooLongError, PasswordTooLongError, EmailTooLongError, InvalidEmailError
from entry_task.utils.validate_email import is_valid_email

class RegisterUserDTO:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def validate(self):
        if len(self.username) < 1:
            raise UsernameRequiredError()

        if len(self.password) < 1:
            raise PasswordRequiredError()

        if len(self.email) < 1:
            raise EmailRequiredError()

        if len(self.username) > 32:
            raise UsernameTooLongError()

        if len(self.password) > 32:
            raise PasswordTooLongError()

        if len(self.email) > 50:
            raise EmailTooLongError()
        
        if is_valid_email(self.email) == False:
            raise InvalidEmailError()
        
class LoginDTO:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate(self):
        if len(self.username) < 1:
            raise UsernameRequiredError()

        if len(self.password) < 1:
            raise PasswordRequiredError()
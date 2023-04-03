from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import socket
from entry_task.dto.auth_dto import RegisterUserDTO, LoginDTO
from entry_task.errors.auth_errors import EmailRequiredError, EmailTooLongError, InvalidEmailError, PasswordRequiredError, PasswordTooLongError, UsernameRequiredError, UsernameTooLongError
from entry_task.utils.http_statuses import HTTPStatus
from entry_task.utils.connection_pool import ConnectionPool
from collections import OrderedDict

class AuthViews:
    def __init__(self):
        self.HOST = os.environ.get('TCP_HOST')
        self.PORT = int(os.environ.get('TCP_PORT'))
        self.REGISTER_ACTION = "register"
        self.LOGIN_ACTION = "login"
        self.size = 5
        self.pool = ConnectionPool(self.HOST, self.PORT, self.size)

    @csrf_exempt
    def register(self, request):
        if request.method == 'POST':
            try:   
                body = json.loads(request.body)
                req = RegisterUserDTO(**body)
                req.validate()
                s = self.pool.get_connection()
                payload = {
                    "action": self.REGISTER_ACTION,
                    "data": req.__dict__
                }

                s.sendall(json.dumps(payload))
                response = s.recv(1024)
                data = json.loads(response)

                self.pool.release_connection(s)
                return HttpResponse(json.dumps(data, sort_keys=True), content_type="application/json")
            except (UsernameRequiredError, PasswordRequiredError, EmailRequiredError, UsernameTooLongError, PasswordTooLongError, EmailTooLongError, InvalidEmailError) as e:
                response = OrderedDict([
                    ("code", HTTPStatus.BAD_REQUEST),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.BAD_REQUEST)
            except Exception as e:
                response = OrderedDict([
                    ("code", HTTPStatus.INTERNAL_SERVER_ERROR),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.INTERNAL_SERVER_ERROR)
            finally:
                self.pool.close_all_connections()
        
    @csrf_exempt
    def login(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                req = LoginDTO(**body)
                req.validate()
                s = self.pool.get_connection()

                payload = {
                    "action": self.LOGIN_ACTION,
                    "data": req.__dict__
                }

                s.sendall(json.dumps(payload))
                response = s.recv(1024)
                data = json.loads(response)

                self.pool.release_connection(s)
                return HttpResponse(json.dumps(data), content_type="application/json")
            except (UsernameRequiredError, PasswordRequiredError) as e:
                response = OrderedDict([
                    ("code", HTTPStatus.BAD_REQUEST),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.BAD_REQUEST)
            except Exception as e:
                response = OrderedDict([
                    ("code", HTTPStatus.INTERNAL_SERVER_ERROR),
                    ("message", str(e))
                ])
                return HttpResponse(json.dumps(response), content_type="application/json", status=HTTPStatus.INTERNAL_SERVER_ERROR)
            finally:
                self.pool.close_all_connections()
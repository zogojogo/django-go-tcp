from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from entry_task.dto.auth_dto import RegisterUserDTO, LoginDTO
from entry_task.errors.auth_errors import EmailRequiredError, EmailTooLongError, InvalidEmailError, PasswordRequiredError, PasswordTooLongError, UsernameRequiredError, UsernameTooLongError
from entry_task.errors.general_errors import InternalServerError
from entry_task.utils.http_statuses import HTTPStatus
from entry_task.utils.connection_pool import ConnectionPool
from entry_task.utils.response import response_error_json, response_success_json
from entry_task.proto.user_pb2 import LoginRequest, TCPRequest, TCPResponse, AuthResponse
from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToDict

class AuthViews:
    def __init__(self):
        self.HOST = os.environ.get('TCP_HOST')
        self.PORT = int(os.environ.get('TCP_PORT'))
        self.REGISTER_ACTION = "register"
        self.LOGIN_ACTION = "login"
        self.size = 35
        self.pool = ConnectionPool(self.HOST, self.PORT, self.size)

    @csrf_exempt
    def register(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                req = RegisterUserDTO(**body)
            except:
                return response_error_json("Failed to bind json, invalid request body", HTTPStatus.BAD_REQUEST)
            try:   
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
                return response_error_json(str(e), HTTPStatus.BAD_REQUEST)
            except Exception as e:
                return response_error_json("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)
        
    @csrf_exempt
    def login(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                req = LoginDTO(**body)
            except:
                return response_error_json("Failed to bind json, invalid request body", HTTPStatus.BAD_REQUEST)
            try:
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
                return HttpResponse(json.dumps(data, sort_keys=True), content_type="application/json")
            except (UsernameRequiredError, PasswordRequiredError) as e:
                return response_error_json(str(e), HTTPStatus.BAD_REQUEST)
            except Exception as e:
                return response_error_json(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
            
    @csrf_exempt
    def test(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                req = LoginDTO(**body)
            except:
                return response_error_json("Failed to bind json, invalid request body", HTTPStatus.BAD_REQUEST)
            try:
                req.validate()
                s = self.pool.get_connection()

                login = LoginRequest()
                login.username = req.username
                login.password = req.password

                tcpReq = TCPRequest()
                tcpReq.action = "test"
                tcpReq.data.Pack(login)

                data = tcpReq.SerializeToString()
                s.sendall(data)

                response = s.recv(1024)
                login_response = TCPResponse()
                login_response.ParseFromString(response)
                if login_response.message:
                    return response_error_json(login_response.message, login_response.code)

                auth_response = AuthResponse()
                any_msg = login_response.data
                Any.FromString(any_msg.value).Unpack(auth_response)
                auth_response_json = MessageToDict(auth_response)

                self.pool.release_connection(s)
                return response_success_json(auth_response_json, login_response.code)
            except Exception as e:
                return response_error_json(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)



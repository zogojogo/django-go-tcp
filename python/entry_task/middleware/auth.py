import jwt
import os
from entry_task.utils.http_statuses import HTTPStatus
from entry_task.utils.response import response_error_json
from jwt.exceptions import DecodeError, ExpiredSignatureError

class JWTAuthenticationMiddleware(object):
    def __init__(self):
        self.allowed_paths = [
            '/login/',
            '/register/',
        ]
        self.jwt_secret_key = os.environ.get('JWT_SECRET')

    def process_request(self, request):
        if request.path not in self.allowed_paths:
            jwt_auth_header = request.META.get('HTTP_AUTHORIZATION', None)
            if jwt_auth_header:
                try:
                    jwt_token = jwt_auth_header.split(' ')[1]
                    jwt_decoded = jwt.decode(jwt_token, self.jwt_secret_key, algorithms=['HS256'])

                    if jwt_decoded['user']:
                        request.user = jwt_decoded['user']

                except (DecodeError, ExpiredSignatureError):
                    return response_error_json("Unauthorize", HTTPStatus.UNAUTHORIZED)
                
                except Exception:
                    return response_error_json("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)
            
            else:
                    return response_error_json("Unauthorize", HTTPStatus.UNAUTHORIZED)
    
        return None
                    
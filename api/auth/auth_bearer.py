from ninja.security import HttpBearer
import jwt
import os
from datetime import datetime


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):

        try:
            jwt_options = {
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': False,
                'verify_aud': False
            }
            jwtPayload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'], options=jwt_options)

            if jwtPayload["exp"] < datetime.now().timestamp():
                return False

            return True
        except jwt.exceptions.InvalidAudienceError as e:
            return False
        except jwt.exceptions.InvalidAlgorithmError as e:
            return False
        except jwt.exceptions.DecodeError as e:
            return False
        except jwt.exceptions.InvalidTokenError as e:
            return False
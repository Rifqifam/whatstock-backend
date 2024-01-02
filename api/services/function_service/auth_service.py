from ...exceptions.user_exceptions import AuthFailed, UserAlreadyExist, ResourceAlreadyExist
from ...exceptions.general_exceptions import ResourceNotFound, BadRequest
from .user_service import UserService
from datetime import datetime, timedelta
from dateutil import tz
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
import jwt
import os


class UserAuthService:
    @staticmethod
    def login(email:str, password:str):
        user = UserService.get_user_by_email(email)
        if user == None:
            raise ResourceNotFound("Email not found")

        if pbkdf2_sha256.verify(password, user.password):
            
            sent_payload = {
                "user_id":user.id,
                "email":user.email,
                "exp": timezone.now() + timedelta(hours=24)
            }
            token = jwt.encode(sent_payload, os.environ['SECRET_KEY'])

            user.last_login = timezone.now()
            user.update()

            return 200, "Login succesfull", {
                "access_token":token,
            }
        else:
            raise AuthFailed("Email or password is incorrect")

    def decode_token(auth_token:str):
        auth_token = auth_token.replace('Bearer ','')
        payload = jwt.decode(auth_token, os.environ['SECRET_KEY'], algorithms=['HS256'])
        return payload
# Exceptions
from api.exceptions.user_exceptions import UserAlreadyExist
from api.exceptions.general_exceptions import *

# Model
from api.models.obj.user_model import User, UserInfo

# Library
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from dateutil import tz
from django.utils import timezone
import os


class UserService:
    @staticmethod
    def register_user(email:str, password:str, name:str):
        if UserService.get_user_by_email(email) != None:
            raise UserAlreadyExist(f"{email} already exist")

        user = User()
        user.email = email
        user.password = pbkdf2_sha256.encrypt(password)
        user.name = name
        user.is_google_login = False
        user.created_at = timezone.now()

        user.save()

        return 200, "User created", user.id
    
    @staticmethod
    def set_user_info(user_id, name:str, gender:str, birth_date, social:list):
        available_gender = ['male', 'female', 'other']

        user = UserService.get_user_by_id(user_id)
        if user is None:
            raise ResourceNotFound("User not found")

        if gender not in available_gender:
            raise BadRequest("Set gender to male, female, or other")

        if len(social) != 0:
            pass

        birth_date = datetime.fromtimestamp(birth_date, tz=tz.gettz(os.environ['TIMEZONE']))
        user.name = name

        user.update()

        info_id = f"info-{user.id}"
        user_info = UserInfo.collection.get(f"user_info/{info_id}")

        new_user = False
        if user_info is None:
            user_info = UserInfo()
            user_info.info_id = f"info-{user.id}"
            new_user = True
        
        user_info.user_id = user
        user_info.gender = gender
        user_info.social = social
        user_info.birth_date = birth_date

        if new_user:
            user_info.upsert()
        else:
            user_info.update()

        return 200, "User info set"
    
    @staticmethod
    def get_user_by_id(user_id, serialized = False):
        user = User.collection.get(f"user/{user_id}")
        if not serialized:
            return user
        else:
            return UserService.serialize_user(user)
        
    @staticmethod
    def get_user_by_email(email, serialized=False):
        user = User.collection.filter('email', '==', email).get()
        if not serialized:
            return user
        else:
            return UserService.serialize_user(user)


        

    @staticmethod
    def serialize_user(user):
        if user != None:
            try:
                userinfo = UserInfo.collection.get(f"user_info/info-{user.id}")
                if userinfo != None:
                    userinfo_dict = {
                        "gender":userinfo.gender,
                        "birth_date":userinfo.birth_date,
                        "social":userinfo.social,
                        "has_taken_meq":userinfo.has_taken_meq,
                        "me_type":userinfo.me_type,
                        "theme":userinfo.theme if userinfo.theme != None else "light",
                        "has_taken_tutorial":{
                            "dashboard":userinfo.has_taken_tutorial_dashboard \
                                  if userinfo.has_taken_tutorial_dashboard != None else False,
                            "product":userinfo.has_taken_tutorial_product \
                                  if userinfo.has_taken_tutorial_product != None else False,
                            "bom":userinfo.has_taken_tutorial_bom \
                                  if userinfo.has_taken_tutorial_bom != None else False,
                            "kansei":userinfo.has_taken_tutorial_kansei \
                                  if userinfo.has_taken_tutorial_kansei != None else False,
                            "affinity":userinfo.has_taken_tutorial_affinity \
                                  if userinfo.has_taken_tutorial_affinity != None else False,
                        }
                    }
                else:
                    userinfo_dict = {
                        "gender":None,
                        "birth_date":None,
                        "social":None,
                        "has_taken_meq":None,
                        "me_type":None
                    }
            except:
                userinfo_dict = {
                    "gender":None,
                    "birth_date":None,
                    "social":None,
                    "has_taken_meq":None,
                    "me_type":None
                }

            return {
                "id":user.id,
                "email":user.email,
                "name":user.name,
                "info":userinfo_dict
            }
        else:
            raise ResourceNotFound("User Not Found")
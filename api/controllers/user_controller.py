from ninja import Router, UploadedFile, Form, File

from api.exceptions.user_exceptions import UserAlreadyExist
from api.exceptions.general_exceptions import BadRequest, ResourceNotFound, InternalServerError

# Services
from api.services.function_service.user_service import UserService
from api.services.function_service.auth_service import UserAuthService
from api.auth.auth_bearer import AuthBearer
from api.services.file_upload.storage_service import StorageService

# Schema and Model
from ..models.schema.response_schema import SuccessResponseMessage
from ..models.schema.user_schema import RegisterUser, SetUserInfo


user_api = Router(tags=['User'])



@user_api.post("/register", response={200:SuccessResponseMessage})
def register_user(request, data:RegisterUser):
    try:
        status, message, payload = UserService.register_user(
            email=data.email,
            password=data.password,
            name=data.name
        )

        user = UserService.get_user_by_email(data.email)

        status, message_user_set = UserService.set_user_info(
            user_id=user.id,
            name=data.name,
            gender=data.gender,
            birth_date=data.birth_date,
            social=[]
        )

        return SuccessResponseMessage(
            status=status,
            message=f"{message}, {message_user_set}"
        )
    except UserAlreadyExist as e:
        raise UserAlreadyExist(str(e))
    except BadRequest as e:
        UserService.delete_user(user.id)
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        
        raise InternalServerError(str(e))

@user_api.post("/set-user-info", response={200:SuccessResponseMessage}, auth=AuthBearer())
def set_user_info(request, data:SetUserInfo):
    payload = UserAuthService.decode_token(request.headers['Authorization'])
    try:
        status, message = UserService.set_user_info(
            user_id=payload['user_id'],
            name=data.name,
            gender=data.gender,
            birth_date=data.birth_date,
            social=data.social
        )

        return SuccessResponseMessage(
            status=status,
            message=message
        )
    except UserAlreadyExist as e:
        raise UserAlreadyExist(str(e))
    except BadRequest as e:
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        raise InternalServerError(str(e))
    
@user_api.post("/set-user-profile-image", response={200: SuccessResponseMessage}, auth=AuthBearer())
def set_user_profile_image(request,
        profile_image:UploadedFile = File(None)                       
     ):
    payload = UserAuthService.decode_token(request.headers['Authorization'])
    try:
        status, message= StorageService.upload_file(
            file=profile_image,
            user_id=payload['user_id']
        )

        user = UserService.get_user_by_id(payload['user_id'], serialized=True)  


        return SuccessResponseMessage(
            status=status,
            message=message,
            payload=user
        )
    except UserAlreadyExist as e:
        raise UserAlreadyExist(str(e))
    except BadRequest as e:
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        raise InternalServerError(str(e))
    
@user_api.delete("/delete-user-profile-image", response={200: SuccessResponseMessage}, auth=AuthBearer())
def delete_user_profile_image(request):
    payload = UserAuthService.decode_token(request.headers['Authorization'])
    try:
        file_name = f"{payload['user_id']}-profile-image"

        success, message = StorageService.delete_file(file_name=file_name)

        if success:
            return SuccessResponseMessage(message=message)
        else:
            raise InternalServerError(message)

    except UserAlreadyExist as e:
        raise UserAlreadyExist(str(e))
    except BadRequest as e:
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        raise InternalServerError(str(e))

    
@user_api.get("/info", response={200:SuccessResponseMessage}, auth=AuthBearer())
def get_user_by_id(request):
    payload = UserAuthService.decode_token(request.headers['Authorization'])
    try:
        user = UserService.get_user_by_id(payload['user_id'], serialized=True)        
        return SuccessResponseMessage(
            payload=user
        )
    except UserAlreadyExist as e:
        raise UserAlreadyExist(str(e))
    except BadRequest as e:
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        raise InternalServerError(str(e))
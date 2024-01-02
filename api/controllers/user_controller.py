from ninja import Router

from api.exceptions.user_exceptions import UserAlreadyExist
from api.exceptions.general_exceptions import BadRequest, ResourceNotFound, InternalServerError

# Services
from api.services.function_service.user_service import UserService
from api.services.function_service.auth_service import UserAuthService
from api.auth.auth_bearer import AuthBearer

# Schema and Model
from ..models.schema.response_schema import SuccessResponseMessage
from ..models.schema.user_schema import RegisterUser


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
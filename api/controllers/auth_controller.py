from ninja import Router
from api.exceptions.general_exceptions import BadRequest, InternalServerError, ResourceNotFound

from api.exceptions.user_exceptions import AuthFailed, UserAlreadyExist
from api.models.schema.user_schema import LoginUser
from ..models.schema.response_schema import SuccessResponseMessage
from ..services.function_service.auth_service import UserAuthService


auth_api = Router(tags=['Authentication'])

@auth_api.post("/login", response={200:SuccessResponseMessage})
def login(request, data:LoginUser):
    try:
        status, message, payload = UserAuthService.login(
            email=data.email,
            password=data.password
        )
        return SuccessResponseMessage(
            status = status,
            message = message,
            payload = payload
        )
    except AuthFailed as e:
        raise AuthFailed(str(e))
    except BadRequest as e:
        raise BadRequest(str(e))
    except ResourceNotFound as e:
        raise ResourceNotFound(str(e))
    except Exception as e:
        
        raise InternalServerError(str(e))
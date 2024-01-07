from ninja import NinjaAPI

from .test_route import test_api
from .user_controller import user_api
from .auth_controller import auth_api
from .stock_controller import stock_api

# EXCEPTIONS INCLUDE
from ..exceptions.user_exceptions import *
from ..exceptions.general_exceptions import *

whatstocks_api = NinjaAPI(
    title="WhatStock API",
    description="API connection for WhatStock API ",
    version="0.1.1"
)

whatstocks_api.add_router("/test", test_api)
whatstocks_api.add_router("/login", auth_api)
whatstocks_api.add_router("/user", user_api)
whatstocks_api.add_router("/stocks", stock_api)


@whatstocks_api.exception_handler(ResourceNotFound)
def resource_not_found(request, ex):
    return whatstocks_api.create_response(
        request,
        dict(status=404, message=str(ex)),
        status=404
    )

@whatstocks_api.exception_handler(InternalServerError)
def internal_server_error(request, ex):
    return whatstocks_api.create_response(
        request,
        dict(status=500, message=str(ex)),
        status=500
    )

@whatstocks_api.exception_handler(UserAlreadyExist)
def internal_server_error(request, ex):
    return whatstocks_api.create_response(
        request,
        dict(status=400, message=str(ex)),
        status=400
    )

@whatstocks_api.exception_handler(BadRequest)
def internal_server_error(request, ex):
    return whatstocks_api.create_response(
        request,
        dict(status=400, message=str(ex)),
        status=400
    )

@whatstocks_api.exception_handler(AuthFailed)
def internal_server_error(request, ex):
    return whatstocks_api.create_response(
        request,
        dict(status=401, message=str(ex)),
        status=401
    )

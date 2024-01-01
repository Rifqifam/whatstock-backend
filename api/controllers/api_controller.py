from ninja import NinjaAPI

from .test_route import test_api

whatstocks_api = NinjaAPI(
    title="WhatStock API",
    description="API connection for WhatStock API ",
    version="0.1.1"
)

whatstocks_api.add_router("/test", test_api)
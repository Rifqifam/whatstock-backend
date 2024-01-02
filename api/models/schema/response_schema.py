from ninja import Schema

class SuccessResponseMessage(Schema):
    status:int = 200
    message:str = "OK"
    payload:dict = {}


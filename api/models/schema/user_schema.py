from ninja import Schema


class RegisterUser(Schema):
    email:str
    password:str
    name:str
    gender:str
    birth_date:float

class LoginUser(Schema):
    email:str
    password:str

class SetUserInfo(Schema):
    name:str
    gender:str
    birth_date:float
    social:list = []
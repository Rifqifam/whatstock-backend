from fireo.models import Model
from fireo import fields


class User(Model):
    email = fields.TextField(required=True)
    password = fields.TextField()
    name = fields.TextField(required=True)
    created_at = fields.DateTime(required=True)
    is_google_login = fields.BooleanField(default=False)
    last_login = fields.DateTime()

class UserInfo(Model):
    info_id = fields.IDField()
    user_id = fields.ReferenceField(User)
    gender = fields.TextField()
    birth_date = fields.DateTime()
    social = fields.ListField()
    theme = fields.TextField(default="light")
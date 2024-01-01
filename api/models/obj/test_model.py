from fireo.models import Model
from fireo import fields

class YourModel(Model):
    id = fields.IDField()
    name = fields.TextField()
    description = fields.TextField()
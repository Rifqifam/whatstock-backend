from fireo.models import Model
from fireo import fields

class Stock(Model):
    stock_code = fields.TextField(required=True)
    nama_perusahaan = fields.TextField(required=True)
    tanggal_pencatatan = fields.TextField(required=True)
    papan_pencatatan = fields.TextField(required=True)
    created_at = fields.DateTime(required=True)

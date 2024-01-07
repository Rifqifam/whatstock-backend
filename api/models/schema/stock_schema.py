from ninja import Schema
from typing import List

class RegisterStock(Schema):
    No : int
    Kode : str
    Nama_Perusahaan : str
    Tanggal_Pencatatan : str
    Papan_Pencatatan : str

class BulkRegisterStock(Schema):
    data : List[RegisterStock]
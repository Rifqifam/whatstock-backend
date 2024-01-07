# Exceptions
from api.exceptions.user_exceptions import ResourceAlreadyExist
from api.exceptions.general_exceptions import *

# Model
from api.models.obj.stock_model import Stock

# Library
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from dateutil import tz
from django.utils import timezone
import os
from api.services.file_upload.storage_service import StorageService


class StockService:
    @staticmethod
    def register_stock(stock_code, nama_perusahaan:str, tanggal_pencatatan:str, papan_pencatatan:str):
        if StockService.get_stock_by_stock_id(stock_code) != None:
            raise ResourceAlreadyExist(f"{stock_code} already exists")
        
        stock = Stock()
        stock.stock_code = stock_code
        stock.nama_perusahaan = nama_perusahaan
        stock.tanggal_pencatatan = tanggal_pencatatan
        stock.papan_pencatatan = papan_pencatatan
        stock.created_at = timezone.now()

        stock.save()

        return 200, f"{stock_code} added to database"

    @staticmethod
    def get_stock_by_stock_id(stock_code, serialized=False):
        stock = Stock.collection.filter('stock_code', '==', stock_code).get()
        if not serialized:
            return stock
        else:
            return StockService.serialize_stock(stock)
        
    @staticmethod
    def delete_stock_by_stock_id(stock_code):
        stock = Stock.collection.filter('stock_code', '==', stock_code).get()
        Stock.collection.delete(stock.key)



    @staticmethod
    def serialize_stock(stock):
        if stock != None:
            return{
                "stock_id" : stock.stock_code,
                "nama perusahaan" : stock.nama_perusahaan,
                "tanggal pencatatan" : stock.tanggal_pencatatan,
                "papan pencatatan" : stock.papan_pencatatan
            }
        else:
            raise ResourceNotFound("Stock Not Found")
        
    



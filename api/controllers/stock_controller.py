from ninja import Router, UploadedFile, Form, File
from typing import List, Dict

from api.exceptions.user_exceptions import UserAlreadyExist
from api.exceptions.general_exceptions import BadRequest, ResourceNotFound, InternalServerError

# Services
from api.services.function_service.stock_service import StockService
from api.services.function_service.auth_service import UserAuthService
from api.auth.auth_bearer import AuthBearer
from api.services.file_upload.storage_service import StorageService

# Schema and Model
from ..models.schema.response_schema import SuccessResponseMessage
from ..models.schema.stock_schema import RegisterStock, BulkRegisterStock



stock_api = Router(tags=['Stock'])

@stock_api.post("/register", response={200: SuccessResponseMessage}, auth=AuthBearer(), description="")
def register_stocks(request, data: BulkRegisterStock):
    """
    Register multiple stocks.

    Example Request Body:
    ```json
    {
      "data": [
        {
          "No": 2,
          "Kode": "ABBA",
          "Nama_Perusahaan": "Mahaka Media Tbk.",
          "Tanggal_Pencatatan": "03 Apr 2002",
          "Papan_Pencatatan": "Pemantauan Khusus"
        },
        {
          "No": 3,
          "Kode": "ABDA",
          "Nama_Perusahaan": "Asuransi Bina Dana Arta Tbk.",
          "Tanggal_Pencatatan": "06 Jul 1989",
          "Papan_Pencatatan": "Pemantauan Khusus"
        }
      ]
    }
    ```

    Returns:
    - 200: Success message
    """

    response_messages = []

    for stock_data in data.data:
        try:
            status, message = StockService.register_stock(
                stock_code=stock_data.Kode,
                nama_perusahaan=stock_data.Nama_Perusahaan,
                tanggal_pencatatan=stock_data.Tanggal_Pencatatan,
                papan_pencatatan=stock_data.Papan_Pencatatan
            )

            response_messages.append({
                'status': status,
                'message': f"{message}, {stock_data.Kode} added"
            })
        except UserAlreadyExist as e:
            raise UserAlreadyExist(str(e))
        except ResourceNotFound as e:
            raise ResourceNotFound(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    return response_messages
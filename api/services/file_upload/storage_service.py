from google.cloud import storage
from api.exceptions.general_exceptions import ResourceNotFound, InternalServerError, BadRequest
import uuid

import os

MAX_FILE_SIZE = 3_000_000

class StorageService:
    def upload_file(file, user_id, file_name = None):
        try:
            file_type = file.name.split('.')[-1]
            if file_name == None:
                file_name = f"{user_id}-profile-image.{file_type}"
            
            data = file.file
            
            StorageService.validate_file_image(file)
            client = storage.Client()
            bucket = client.bucket(os.environ['STORAGE_BUCKET'])
            file_blob = bucket.blob(file_name)
            file_blob.content_type = file.content_type
            file_blob.upload_from_file(data)
            file_blob.make_public()

            return 200, "File Upload Success"
        except BadRequest as e:
            raise BadRequest(str(e))
        except Exception as e:
            print(f"Error : {e}")
            raise InternalServerError(f"Failed to upload {file_name}")
           

    def validate_file_image(image_file):
        if image_file.size > MAX_FILE_SIZE:
            raise BadRequest("Maximum file is 3MB")
        if image_file.content_type != 'image/png' and image_file.content_type != 'image/jpeg':
            raise BadRequest("Image file must be in jpg or png format")

    def delete_file(file_name):
        try:
            client = storage.Client()
            bucket = client.bucket(os.environ['STORAGE_BUCKET'])

            file_name_jpg = file_name + '.jpg'
            file_blob_jpg = bucket.blob(file_name_jpg)
            if file_blob_jpg.exists():
                file_blob_jpg.delete()
                return True, "File Deleted Successfully (JPEG)"

            file_name_png = file_name + '.png'
            file_blob_png = bucket.blob(file_name_png)
            if file_blob_png.exists():
                file_blob_png.delete()
                return True, "File Deleted Successfully (PNG)"
            
            return False, f"{file_name} Not Found"
        except (ValueError, AttributeError) as e:
            print(str(e))
            return False, str(e)
        except Exception as e:
            print(str(e))
            raise InternalServerError(str(e))

        
from ninja import Router
from django.http import JsonResponse
from firebase_admin import firestore

from ..models.obj.test_model import YourModel

test_api = Router(tags=['Endpoint Test'])

@test_api.get("/endpoint")
def test_Endpoint(request):
    return {"message": "Hello, Django Ninja!"}

@test_api.post("/test_db")
def test_db(request):
    model = YourModel()

    model.id = "1" 
    model.name = "test insert"
    model.description = f"test insert-{model.id}"
    model.upsert()

    return 200, "Board updated"

@test_api.get("/get_test_db")
def get_test_db(request):
    # Retrieve all data from the Firestore collection
    all_data = YourModel.collection.fetch()

    # Convert the data to a list of dictionaries
    data_list = [doc.to_dict() for doc in all_data]

    return {"message": "Data retrieved successfully", "data": data_list}








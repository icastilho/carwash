import uuid

from flask_injector import inject

from services.firestore import Firestore
from services.washer import Washer

class Brand(object):

    @inject
    def start(self, washer: Washer) -> bool:
        return washer.wash_brands(), 201

    @inject
    def search(self, firestore: Firestore) -> list:
        return firestore.list('vehicles/brands/'), 201

    @inject
    def post(self, firestore: Firestore, brand: dict) -> dict:
        firestore.create(brand,'vehicles/brands/')
            # return {"error": "Car index erro"}, 400
        return brand, 201

class_instance = Brand()

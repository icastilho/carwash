import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from injector import Scope
from flask import current_app
from flask_injector import inject

class Firestore(object):
    @inject
    def __init__(self, path, databaseURL,):
        firebase_admin.initialize_app(credentials.Certificate(path), {
            'databaseURL': databaseURL
        })

    def create(self, dict: dict, path):
        ref = db.reference(path + dict['id'])
        ref.update(dict)

    def list(self, path) -> list:
        return db.reference(path).get()

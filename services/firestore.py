import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from injector import Scope

firebase_admin.initialize_app(credentials.Certificate('autoslances-e361125943e1.json'), {
    'databaseURL': 'https://autoslances.firebaseio.com'
})

class Firestore(object):

    def create(self, dict: dict, path):
        ref = db.reference(path + dict['id'])
        ref.update(dict)

    def list(self, path) -> list:
        return db.reference(path).get()

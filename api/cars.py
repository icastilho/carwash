import uuid
from flask import render_template
from flask_injector import inject
from services.washer import Washer

class Car(object):

    @inject
    def start(self, washer: Washer) -> dict:
        execution=washer.start()
        if execution:
            return {'SUCCESS':'Car Wash was Successfully executed'}, 201
        else:
            return {"error": "Car Wash Erro"}, 400

    @inject
    def delete(self, washer: Washer) -> dict:
        execution=washer.delete()
        if execution:
            return {'SUCCESS':'Delete Index was Successfully executed'}, 201
        else:
            return {"error": "Delete index Erro"}, 400

    @inject
    def version(self, washer: Washer) -> dict:
        execution=washer.wash_versions()
        if execution:
            return {'SUCCESS':'Version Index Successfully executed'}, 201
        else:
            return {"error": "Version Index Erro"}, 400

    @inject
    def model(self, washer: Washer) -> dict:
        execution=washer.wash_models()
        if execution:
            return {'SUCCESS':'Model Index Successfully executed'}, 201
        else:
            return {"error": "Model Index Erro"}, 400


class_instance = Car()

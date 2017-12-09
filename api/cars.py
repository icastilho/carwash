import uuid
from flask import render_template
from flask_injector import inject
from services.washer import Washer
from flask import current_app

class Car(object):

    @inject
    def start(self, washer: Washer) -> dict:
        execution=washer.start()
        if execution:
            return {'SUCCESS':'Car Wash was Successfully executed'}, 201
        else:
            return {"error": "Car Wash Erro"}, 400

    @inject
    def delete(self, washer: Washer, index_name: dict) -> dict:
        current_app.logger.info('Deleting ...', index_name)
        execution=washer.delete(index_name)
        if execution:
            return {'SUCCESS':'Delete Index was Successfully executed'}, 201
        else:
            return {"error": "Delete index Erro"}, 400

    @inject
    def version(self, washer: Washer) -> dict:
        execution=washer.wash_versions(washer.loadData())
        if execution:
            return {'SUCCESS':'Version Index Successfully executed'}, 201
        else:
            return {"error": "Version Index Erro"}, 400

    @inject
    def model(self, washer: Washer) -> dict:
        execution=washer.wash_models(washer.loadData())
        if execution:
            return {'SUCCESS':'Model Index Successfully executed'}, 201
        else:
            return {"error": "Model Index Erro"}, 400

    @inject
    def vehicle(self, washer: Washer) -> dict:
        execution=washer.wash_vehicles(washer.loadData())
        if execution:
            return {'SUCCESS':'vehicle Index Successfully executed'}, 201
        else:
            return {"error": "vehicle Index Erro"}, 400


class_instance = Car()

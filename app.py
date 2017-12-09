import os
import connexion
import logging

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver
from logging.handlers import RotatingFileHandler

from services.elasticsearch import ElasticSearchIndex, ElasticSearchFactory
from conf.elasticsearch_mapper import vehicle_mapping, brand_mapping, model_mapping, version_mapping
from services.firestore import Firestore
from services.washer import Washer

def configure(binder: Binder) -> Binder:
    binder.bind(Firestore)
    binder.bind(Washer)

    binder.bind(
            ElasticSearchIndex,
            ElasticSearchIndex(
                ElasticSearchFactory(''),
                {'vehicles': vehicle_mapping, 'brands': brand_mapping, 'models': model_mapping, 'versions': version_mapping}
            )
    )

    return binder

def configure_log(app):
    app.debug = True
    # initialize the log handler
    logHandler = RotatingFileHandler('log/info.log', maxBytes=1000, backupCount=1)
    # set the log handler level
    logHandler.setLevel(logging.INFO)
    # set the app logger level
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logHandler)


if __name__ == '__main__':
    app = connexion.App(__name__,  specification_dir='swagger/')
    app.add_api('carwash.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    configure_log(app.app)
    app.run(port=9090)
    app.app.logger.info("Car Wash was started!!!")

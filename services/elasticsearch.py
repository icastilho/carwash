import re
from flask import current_app
from flask_injector import inject
from elasticsearch import Elasticsearch

class ElasticSearchFactory(object):

    def __init__(self, bonsaiUrl):
        self.url = bonsaiUrl


    def create(self) -> Elasticsearch:
        # Parse the auth and host from env:
        # bonsai = os.environ['BONSAI_URL']
        bonsai = self.url

        # Connect to cluster over SSL using auth for best security:
        es_header = [{
          'host': 'localhost',
          'port': 9200,
          'use_ssl': True,
          'protocol': 'http',
          'verify_certs':False
        }]

        # Instantiate the new Elasticsearch connection:
        es = Elasticsearch(es_header)

        # Verify that Python can talk to Bonsai (optional):
        current_app.logger.info('Bonsai ping...', es.ping())
        return es


class ElasticSearchIndex(object):
    @inject
    def __init__(
            self,
            elastic_factory: ElasticSearchFactory,
            indexs,
    ):
        self.indexs = indexs
        self.elastic_factory = elastic_factory
        self.instance = None

    def connection(self) -> Elasticsearch:
        if not self.instance:
            self.instance = self.elastic_factory.create()
            self.createAll()
        return self.instance

    def create(self, index_name) -> bool:
        current_app.logger.info("Creating Index '%s' " % (index_name))
        if not self.instance.indices.exists(index_name):
            self.instance.indices.create(
                index=index_name,
                body=self.indexs[index_name]
            )
            return True
        return False

    def createAll(self):
        for index_name in self.indexs.keys():
            self.create(index_name)

    def index(self, payload: dict, index_name, doc_type) -> bool:
        return self.connection().index(
            index=index_name,
            doc_type=doc_type,
            body=payload
        )

    def delete(self, index_name) -> bool:
        current_app.logger.info("Index '%s' deleting... " % (index_name))
        if self.connection().indices.exists(index_name):
            if self.instance.indices.delete(index_name):
                current_app.logger.info("Index '%s' successfully deleted " % (index_name))
                return True
        else:
            current_app.logger.info("Index '%s' doens't existes! " % (index_name))
        return True

    def deleteAll(self):
        for index_name in self.indexs.keys():
            self.delete(index_name)

    def bulk(self, bulk_data, index_name: str, doc_type: str) -> bool:
        # bulk index the data
        current_app.logger.info("bulk '%s' indexing..." % (index_name))
        res = self.connection().bulk(index = index_name, doc_type=doc_type, body = bulk_data, refresh = True)
        current_app.logger.info("Bulk index the data response: '%s'" % (res))
        return True

    def exists_by_url(self, url: str, index_name, doc_type) -> bool:
        matches = self.connection().search(
            index=index_name,
            doc_type=doc_type,
            body={
                "query": {
                    "query_string": {
                        "query": 'modelo:"{}"'.format(url)
                    }
                }
            }
        )

        hits = matches['hits']['hits']

        if hits:
            return True

        return False

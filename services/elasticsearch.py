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
        auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
        host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

        # Connect to cluster over SSL using auth for best security:
        es_header = [{
          'host': host,
          'port': 443,
          'use_ssl': True,
          'http_auth': (auth[0],auth[1])
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
            index_name: str,
            doc_type: str,
            index_mapper: dict
    ):
        self.index_name = index_name
        self.index_mapper = index_mapper
        self.doc_type = doc_type
        self.elastic_factory = elastic_factory
        self.instance = None

    def connection(self) -> Elasticsearch:
        if not self.instance:
            self.instance = self.elastic_factory.create()
            self.create()
        return self.instance

    def create(self) -> bool:
        current_app.logger.info("Creating Index '%s' " % (self.index_name))
        if not self.instance.indices.exists(self.index_name):
            self.instance.indices.create(
                index=self.index_name,
                body=self.index_mapper
            )
            return True
        return False

    def index(self, payload: dict) -> bool:
        return self.connection().index(
            index=self.index_name,
            doc_type=self.doc_type,
            body=payload
        )

    def delete(self) -> bool:
        current_app.logger.info("Index '%s' deleting... " % (self.index_name))

        if self.connection().indices.exists(self.index_name):
            if self.instance.indices.delete(self.index_name):
                current_app.logger.info("Index '%s' successfully deleted " % (self.index_name))
                return True
        else:
            current_app.logger.info("Index '%s' doens't existes! " % (self.index_name))
        return True

    def bulk(self, bulk_data, index_name: str, doc_type: str) -> bool:
        # bulk index the data
        current_app.logger.info("bulk '%s' indexing..." % (index_name))
        res = self.connection().bulk(index = self.index_name, doc_type=doc_type, body = bulk_data, refresh = True)
        current_app.logger.info("Bulk index the data response: '%s'" % (res))
        return True

    def exists_by_url(self, url: str) -> bool:
        matches = self.connection().search(
            index=self.index_name,
            doc_type=self.doc_type,
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

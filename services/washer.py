import datetime
import pandas as pd
from flask_injector import inject
from injector import Scope
from flask import current_app
from dateutil.relativedelta import relativedelta


from services.firestore import Firestore
from services.elasticsearch import ElasticSearchIndex

class Washer(object):
    @inject
    def __init__(self, firestore: Firestore, elastic: ElasticSearchIndex):
        self.firestore = firestore
        self.elastic = elastic

    def wash_brands(self,data):
       # Load brand data to wash
       current_app.logger.info('Start wash brands!!!')
       brand = pd.DataFrame(data={'id':data['marca_id'], 'name':data['marca']})
       brands_df = brand.groupby(['id']).first()
       brands_df.to_csv('data/brands_test.csv')
    #    brands_df = pd.read_csv('data/brands.csv')
       # Cast id to int

       #load market share values, it will be used to sort search results
       market_shere_df = pd.read_csv('data/market_share.csv')
       #Merge marketshare values
       brand_mege = pd.merge(brands_df, market_shere_df, how='left')
       brand_mege = brand_mege.fillna(0)
       return self.bulk(brand_mege, self.elastic.index_name, 'brand')
       #transform to dict
    #    brands = brand_mege.to_dict(orient='records')


    #    for brand in brands:
    #         current_app.logger.info("brand '%s' " % (brand))
    #         self.firestore.create(brand,'vehicles/brands/')
    #    current_app.logger.debug('Finish wash brands!')

    def wash_models(self, data) -> bool:
        # Load model data to wash
        current_app.logger.info('Start wash models!!!')
        # model_df = pd.read_csv('data/models.csv')
        model_df = pd.DataFrame(data={'id':data['modelo_id'], 'desc':data['modelo'], 'year': data['anomod'], 'brand': data['marca'], 'value':data['valor'] })
        #limpa descrição
        dfmodelo_clean = model_df.join(model_df['desc'].str.extract('(?P<model>^[^\W]+)(?P<version>.*)', expand=True))
        #dfmodelo_clean.loc[dfmodelo_clean['model'].isnull()]
        # Executa regex para modelos que não foram detectados por nao ter a versão
        #substitui os nulos pela descrição inicial
        #dfmodelo_clean['model'].fillna(dfmodelo_clean['desc'].str.extract('(?P<model>^[^\W]+)'), inplace=True)
        dfmodelo_clean['model'] = dfmodelo_clean['model'].str.title()
        # chama wash_version porque os modulos são dependentes de pate da mesma manipulação de dados
        self.wash_versions(dfmodelo_clean)
        # Limpa as colunas que não são necessárias
        csvmodelo = dfmodelo_clean.drop(['version', 'id', 'value', 'desc'], axis=1)
        #Agrupa por modelo
        grouped = csvmodelo.groupby(['model', 'year'],as_index=False).first()
        #Salva no csv
        grouped.to_csv('data/models_test.csv',index=False)

        return self.bulk(grouped, self.elastic.index_name, 'model')

    def wash_versions(self, data) -> bool:
       # Load version data to wash
       current_app.logger.info('Start wash versions!!!')
       #  version_df = pd.read_csv('data/versions.csv')

       #remove desc que não será necessário para versão
       version_df = data.drop('desc', axis=1)
       version_df.to_csv('data/versions_test.csv', index=False)
       return self.bulk(version_df, self.elastic.index_name, 'version')

    def wash_vehicles(self, data) -> bool:
        #Index vehicles
        current_app.logger.info('Start index vehicles!!!')
        # vehicle_df = pd.read_csv('data/vehicles.csv')
        #vehicles = vehicle_df.to_dict(orient='records')
        return self.bulk(data, self.elastic.index_name, 'vehicle')

    def bulk(self, df, index_name: str, doc_type: str) -> bool:
        bulk_data = []
        for index, row in df.iterrows():
            data_dict = {}
            for i in range(len(row)):
                data_dict[df.columns[i]] = row[i]

            op_dict = {
            "index": {
                "_index": index_name,
                "_type": doc_type,
              }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

        if not self.elastic.bulk(bulk_data, index_name, doc_type):
            current_app.logger.error("Error indexing '%s' " % (index_name))
            return false

        return True

    def delete(self):
        return self.elastic.delete()

    def start(self) -> dict:
        current_app.logger.info("Start Clean Wash!!!")
        #clean index_name
        self.elastic.delete()
        #clean index_name
        self.elastic.create()
        # Carregando os dados de treinamento e de testes
        train_df = pd.read_csv('data/fipe_201711_Carro.csv')
        # Filtra os ultimos 10 anos
        years_ago = datetime.datetime.now() - relativedelta(years=5)
        data=train_df[(train_df.anomod >= years_ago.year)]

        #res = self.wash_vehicles(data)
        self.wash_brands(data)
        self.wash_models(data)

        current_app.logger.info("Finish Clean Wash!!!")
        return True

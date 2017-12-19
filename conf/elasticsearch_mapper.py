vehicle_mapping = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    },
    "mappings" : {
        "vehicle": {
            "properties": {
                "fipe_cod": {"type": "text"},
                "tabela_id": {"type": "text"},
                "anoref": { "type": "integer"},
                "mesref": { "type": "integer"},
                "tipo": { "type": "text"},
                "marca_id": { "type": "text"},
                "marca": { "type": "text"},
                "modelo_id": { "type": "text"},
                "descricao": {"type": "text"},
                "anomod": {"type": "text"},
                "comb_cod": {"type": "text"},
                "comb_sigla": {"type": "text"},
                "comb":{"type": "text"},
                "valor":{"type": "text"},
                "modelo":{"type": "text"},
                "versao":{"type": "text"}
            }
        },
    }
}


brand_mapping = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    },
    "mappings" : {
        "brand" : {
            "properties" : {
                "name" : { "type" : "text",
                    "fields": {
                         "keyword": {
                               "type": "keyword",
                               "ignore_above": 256
                           }
                     }
                 },
                "market_share" : { "type" : "integer" },
                "suggest": {
                    "type": "completion"
                }
            }
        }
    }
}

model_mapping = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    },
    "mappings" : {
        "model" : {
            "properties" : {
                "year" : { "type" : "integer" },
                "brand" : {
                            "type": "text",
                            "fields": {
                                 "keyword": {
                                       "type": "keyword",
                                       "ignore_above": 256
                                   }
                             }
                           },
                "model" : {
                            "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
                "suggest": {
                               "type": "completion"
                            }
            }
        }
    }
}

version_mapping = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    },
    "mappings" : {
        "version" : {
            "properties" : {
                "year" : { "type" : "integer" },
                "brand" : {
                    "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                },
                "model" : {
                    "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                 },
                "version" : {
                    "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                 },
                "suggest": {
                               "type": "completion"
                            }
            }
        }
    }
}

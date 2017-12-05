vehicle_mapping = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    },
    "mappings" : {
        "vehicle": {
            "properties": {
                "fipe_cod": {"type": "string"},
                "tabela_id": {"type": "string"},
                "anoref": { "type": "string"},
                "mesref": { "type": "string"},
                "tipo": { "type": "string"},
                "marca_id": { "type": "string"},
                "marca": { "type": "string"},
                "modelo_id": { "type": "string"},
                "descricao": {"type": "string"},
                "anomod": {"type": "string"},
                "comb_cod": {"type": "string"},
                "comb_sigla": {"type": "string"},
                "comb":{"type": "string"},
                "valor":{"type": "string"},
                "modelo":{"type": "string"},
                "versao":{"type": "string"}
            }
        },
        "brand" : {
            "properties" : {
                "name" : { "type" : "text" },
                "market_share" : { "type" : "string" },
                "suggest": {
                               "type": "completion"
                            }
            }
        },
        "model" : {
            "properties" : {
                "year" : { "type" : "integer" },
                "brand" : { "type" : "string" },
                "model" : { "type" : "string" },
                "suggest": {
                               "type": "completion"
                            }
            }
        },
        "version" : {
            "properties" : {
                "year" : { "type" : "integer" },
                "brand" : { "type" : "string" },
                "model" : { "type" : "string" },
                "version" : { "type" : "string" },
                "suggest": {
                               "type": "completion"
                            }
            }
        }
    }
}



#Auctions mappings
auctions_mapping = {
    "settings" : {
        "index" : {
            "number_of_shards" : 2,
            "number_of_replicas" : 1
        }
    },
        "mappings": {
          "auction": {
            "properties": {
              "creationDate": {
                "type": "date"
              },
              "duration": {
                "properties": {
                  "date": {
                    "type": "long"
                  },
                  "name": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "purchase": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              },
              "rating": {
                "properties": {
                  "seller": {
                    "properties": {
                      "comment": {
                        "type": "text",
                        "fields": {
                          "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                          }
                        }
                      },
                      "creationDate": {
                        "type": "long"
                      },
                      "rating": {
                        "type": "long"
                      }
                    }
                  }
                }
              },
              "salesman": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              },
              "selection": {
                "properties": {
                  "brand": {"type": "keyword"}
                  },
                  "cities": {
                    "properties": {
                      "checked": {
                        "type": "boolean"
                      },
                      "count": {
                        "type": "long"
                      },
                      "id": {
                        "type": "text",
                        "fields": {
                          "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                          }
                        }
                      },
                      "name": {"type": "keyword"}
                      },
                      "state": {
                        "type": "text",
                        "fields": {
                          "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                          }
                        }
                      }
                    }
                  },
                  "duration": {
                    "type": "long"
                  },
                  "model": {"type": "keyword"},
                  "options": {"type": "keyword"},
                  "state": {
                    "properties": {
                      "count": {
                        "type": "long"
                      },
                      "id": {
                        "type": "long"
                      },
                      "name": {"type": "keyword"},
                      "uf": {
                        "type": "text",
                        "fields": {
                          "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                          }
                        }
                      }
                    }
                  },
                  "value": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "version": {"type": "keyword"},
                  "year": {
                    "type": "long"
                  }
                }
              },
              "state": {"type": "keyword"},
              "status": {"type": "keyword"},
              "user": {
                "properties": {
                  "displayName": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "email": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  },
                  "uid": {
                    "type": "text",
                    "fields": {
                      "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                      }
                    }
                  }
                }
              },
              "vehicleaspayment": {
                "type": "boolean"
              }
            }
          }
        }
      }


#
autoslances_mapping = {
    "settings" : {
        "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
        }
    },
    "mappings" : {
            "user": {
                  "_all":       { "enabled": "false"  },
                  "properties": {
                    "name":    { "type": "text"  },
                    "email":     { "type": "text"  },
                    "age":      { "type": "integer" },
                    "uid": { "type" : "keyword" },
                     "suggest": {
                         "type": "completion"
                      }
                  }
                }
        }
}

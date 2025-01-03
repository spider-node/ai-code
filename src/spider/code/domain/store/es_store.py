import json

from elasticsearch import Elasticsearch
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


class ESStore:
    def __init__(self):
        with open("spider_config.json", "r", encoding="utf-8") as f:
            configs = json.load(f)
            self.es = Elasticsearch([{"host": configs['es.host'], "port": configs['es.port'],
                                      "username": configs['es.username'], "password": configs['es.password']}])

            self.vector_store = ElasticsearchStore(
                es_client=self.es, index_name="domain_knowledge"
            )

    def query_store(self):
        return self.vector_store

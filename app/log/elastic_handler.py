from datetime import datetime
import json
import logging
import time
from elasticsearch import Elasticsearch


class ElasticHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.es = Elasticsearch('http://127.0.0.1:9200')

    def emit(self, record):
        try:
            index_name = f'log_date{time.strftime("%Y_%m_%d")}'
            self.es.index(index=index_name, document=record.msg)
        except Exception:
            self.handleError(record)

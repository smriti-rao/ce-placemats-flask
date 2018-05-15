import logging
from app.placemats.mongo_store import MongoStore
import os
import pymongo

logger = logging.getLogger(__name__)

store_class = MongoStore


def get_store(resource_name):
    if store_class is MongoStore:
        if 'MONGO_URL' in os.environ:
            url = os.environ['MONGO_URL']
        else:
            url = 'mongodb://localhost:27017/'
        return MongoStore(pymongo.MongoClient(url)['placemats'][resource_name])

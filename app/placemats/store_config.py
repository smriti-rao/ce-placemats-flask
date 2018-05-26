import logging
from app.placemats.mongo_store import MongoStore
from app.placemats.store import BaseStore
import os
import pymongo

logger = logging.getLogger(__name__)

store_class = MongoStore


def _get_store(resource_name) -> BaseStore:
    if store_class is MongoStore:
        if 'MONGO_URL' in os.environ:
            url = os.environ['MONGO_URL']
        else:
            url = 'mongodb://127.0.0.1:27017/'
        return MongoStore(pymongo.MongoClient(url)['placemats'][resource_name],
                          '/{}/'.format(resource_name))


def layouts_store():
    return _get_store('layouts')


def widgets_store():
    return _get_store('widgets')

from app.placemats.stores.cache import BaseCache
from app.placemats.stores.mongo_store import MongoStore
import pymongo.collection
import datetime


class MongoCache(BaseCache):
    def __init__(self, collection: pymongo.collection.Collection, ttl=300) -> None:
        super().__init__()
        self.store = MongoStore(collection)
        collection.create_index('created', expireAfterSeconds=ttl)

    def get(self, key=None):
        doc = self.store.get(pk=key)
        if doc and 'data' in doc:
            return doc['data']
        return None

    def set(self, key=None, data: dict = None):
        doc = {'created': datetime.datetime.utcnow(), 'data': data}
        self.store.add(doc, pk=key)

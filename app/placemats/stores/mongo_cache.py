from app.placemats.stores.cache import BaseCache
import pymongo.collection


class MongoCache(BaseCache):
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        super().__init__()
        self.coll = collection

    def get(self, key=None):
        pass

    def set(self, key=None, data=None, ttl=None):
        pass

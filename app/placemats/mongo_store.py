from app.placemats.store import BaseStore
from bson.objectid import ObjectId
import pymongo.collection
import pymongo.errors
import logging

logger = logging.getLogger(__name__)


class MongoStore(BaseStore):
    def __init__(self, collection: pymongo.collection.Collection, use_object_id=False) -> None:
        super().__init__()
        self.client = collection
        self.use_object_id = use_object_id

    def get(self, pk=None, pks=None, projection=None):
        if pk is not None:
            return self.client.find_one({'_id': self._get_id(pk)})
        find_query = {}
        if pks is not None:
            find_query['_id'] = {'$in': [self._get_id(pk) for pk in pks]}
        return [d for d in self.client.find(find_query, projection=projection)]

    def add(self, to_add, pk=None):
        if pk is not None:
            to_add['_id'] = self._get_id(pk)
        elif not self.use_object_id:
            raise MongoStoreException()  # must use ObjectId's if you're not specifying pk
        try:
            new_pk = self.client.insert_one(to_add).inserted_id
            return True, self.client.find_one({'_id': new_pk})
        except pymongo.errors.DuplicateKeyError:
            if pk is not None:
                return False, self.client.find_one({'_id': to_add['_id']})
            raise MongoStoreException()  # can't handle duplicate keys for non-_id case

    def _get_id(self, pk):
        if self.use_object_id:
            return pk if isinstance(pk, ObjectId) else ObjectId(pk)
        return pk


class MongoStoreException(Exception):
    pass

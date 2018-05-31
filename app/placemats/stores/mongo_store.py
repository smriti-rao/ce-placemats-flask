from app.placemats.stores.store import BaseStore
import pymongo.collection
import pymongo.errors
import logging
import uuid
import urllib.parse
from typing import Tuple

logger = logging.getLogger(__name__)


class MongoStore(BaseStore):
    def __init__(self, collection: pymongo.collection.Collection, href_prefix=None) -> None:
        super().__init__()
        self.client = collection
        self.href_prefix = href_prefix

    def get(self, pk=None, pks: list = None, projection=None, skip=0, limit=0):
        if pk is not None:
            return self.client.find_one({'_id': pk}, projection=projection)
        find_query = {}
        if pks is not None:
            find_query['_id'] = {'$in': pks}
        out = [d for d in self.client.find(find_query, projection=projection, skip=skip, limit=limit)]
        if pks is not None:
            try:
                out = sorted(out, key=lambda d: pks.index(d['_id']))
            except ValueError:
                raise MongoStoreException()
        return out

    def add(self, to_add, pk=None) -> Tuple[bool, dict]:
        to_add['_id'] = str(uuid.uuid4()) if pk is None else pk
        if self.href_prefix is not None:
            to_add['href'] = '{}{}'.format(self.href_prefix, urllib.parse.quote(to_add['_id'], safe=''))
        try:
            new_pk = self.client.insert_one(to_add).inserted_id
            return True, self.client.find_one({'_id': new_pk})
        except pymongo.errors.DuplicateKeyError:
            if pk is not None:
                return False, self.client.find_one({'_id': to_add['_id']})
            raise MongoStoreException()


class MongoStoreException(Exception):
    pass

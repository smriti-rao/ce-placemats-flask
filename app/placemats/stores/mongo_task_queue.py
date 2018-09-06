from app.placemats.stores.task_queue import BaseTaskQueue, TASK_INIT, TASK_PENDING, TASK_FAILED, TASK_SUCCEEDED
from app.placemats.stores.mongo_cache import MongoCache
import pymongo.collection
from pymongo import ReturnDocument
import time
import uuid
from typing import Tuple
import os
import logging

logger = logging.getLogger(__name__)


def get_queue_ttl():
    return int(os.getenv('TASK_QUEUE_TTL', '86400'))


class MongoTaskQueue(BaseTaskQueue):
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        super().__init__()
        self.coll = collection
        self.cache = MongoCache(self.coll, ttl=get_queue_ttl())

    def enqueue(self, idempotency_key: str, task_info: dict):
        self.cache.set(key=idempotency_key, data={
            'task_info': task_info,
            'state': TASK_INIT,
        })

    def dequeue(self) -> Tuple[str, str, dict]:
        while True:
            token = str(uuid.uuid4())
            d = self.coll.find_one_and_update(
                {'data.state': TASK_INIT}, {'$set': {'data.state': TASK_PENDING, 'data.token': token}},
                return_document=ReturnDocument.AFTER)
            if d is None:
                time.sleep(0.15)
                continue
            return d['_id'], token, d['data']['task_info']

    def done(self, idempotency_key: str, token: str, exception: Exception = None, should_reset_task: bool = False):
        if should_reset_task:
            self.coll.find_one_and_update(
                {'_id': idempotency_key, 'data.state': TASK_PENDING, 'data.token': token},
                {'$set': {'data.state': TASK_INIT}})
            return
        if exception is not None:
            logger.error('Deleting failed task. Error: %s , Key: %s', exception, idempotency_key)
        self.coll.find_one_and_delete({'_id': idempotency_key, 'data.state': TASK_PENDING, 'data.token': token})

from app.placemats.task_queue import TaskQueue
from collections import namedtuple
import pymongo.collection

Task = namedtuple('Task', ['idempotency_key', 'task_info', 'state'])

TASK_INIT = 'init'
TASK_PENDING = 'pending'
TASK_FAILED = 'failed'
TASK_SUCCEEDED = 'succeeded'


class MongoTaskQueue(TaskQueue):
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        super().__init__()
        self.coll = collection

    def enqueue(self, idempotency_key, task_info):
        pass

    def dequeue(self):
        pass

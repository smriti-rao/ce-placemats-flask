from app.placemats.task_queue import TaskQueue
import pymongo.collection


class MongoTaskQueue(TaskQueue):
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        super().__init__()
        self.coll = collection

    def enqueue(self, idempotency_key, task_info):
        pass

    def dequeue(self):
        pass

from app.placemats.stores.task_queue import TaskQueue, Task
import pymongo.collection


class MongoTaskQueue(TaskQueue):
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        super().__init__()
        self.coll = collection

    def enqueue(self, task: Task):
        pass

    def dequeue(self) -> Task:
        pass

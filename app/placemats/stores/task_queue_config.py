from app.placemats.stores.task_queue import BaseTaskQueue
from app.placemats.stores.mongo_task_queue import MongoTaskQueue
from app.placemats.stores.mongo_client import mongo_db


def widgets_task_queue() -> BaseTaskQueue:
    return MongoTaskQueue(mongo_db()['widgets_task_queue_v2'])

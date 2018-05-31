from app.placemats.consumer.consumer import BaseConsumer
from app.placemats.stores.task_queue_config import widgets_task_queue


class WidgetsTaskConsumer(BaseConsumer):

    def __init__(self) -> None:
        super().__init__(widgets_task_queue())

    def consume_one(self, task_info: dict):
        pass

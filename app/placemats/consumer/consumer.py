from app.placemats.stores.task_queue import BaseTaskQueue
import time
import logging

logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self, task_queue: BaseTaskQueue) -> None:
        super().__init__()
        self.q = task_queue

    def consume_one(self, task_info: dict):
        raise NotImplementedError()

    def consume_forever(self):
        while True:
            try:
                idempotency_key, token, task_info = self.q.dequeue()
            except Exception as e:
                logger.error('Exception trying to dequeue task: %s Sleeping...will try again soon', e)
                time.sleep(10)
                continue
            try:
                logger.info('Consuming task: %s', task_info)
                self.consume_one(task_info)
            except Exception as e:
                logger.error('Exception consuming task: %s', e)
                exception = e
            else:
                logger.info('Consumed task successfully')
                exception = None
            try:
                self.q.done(idempotency_key=idempotency_key, token=token, exception=exception)
            except Exception as e:
                logger.error('Error marking task "done": %s', e)

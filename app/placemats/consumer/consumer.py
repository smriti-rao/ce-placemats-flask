import logging

from app.placemats.stores.task_queue import BaseTaskQueue

logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self, task_queue: BaseTaskQueue) -> None:
        super().__init__()
        self.q = task_queue

    def consume_one(self, task_info: dict):
        raise NotImplementedError()

    def consume_forever(self):
        while True:
            idempotency_key, token, task_info = self.q.dequeue()
            try:
                logger.info('Consuming task: %s', task_info)
                self.consume_one(task_info)
            except KeyboardInterrupt as ki:
                logger.info('Received SIGINT while handling task %s; resetting and then will exit', task_info)
                error = ki
            except Exception as e:
                logger.error('Exception consuming task: %s', e)
                error = e
            else:
                logger.info('Consumed task successfully')
                error = None
            interrupted = isinstance(error, KeyboardInterrupt)
            self.q.done(idempotency_key=idempotency_key, token=token, exception=error,
                        should_reset_task=interrupted)
            if interrupted:
                logger.info('Re-raising KeyboardInterrupt')
                raise error

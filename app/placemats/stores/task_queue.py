from typing import Tuple

TASK_INIT = 'init'
TASK_PENDING = 'pending'
TASK_FAILED = 'failed'
TASK_SUCCEEDED = 'succeeded'


class BaseTaskQueue:
    def enqueue(self, idempotency_key: str, task_info: dict):
        raise NotImplementedError()

    def dequeue(self) -> Tuple[str, str, dict]:
        raise NotImplementedError()

    def done(self, idempotency_key: str, token: str, exception: Exception = None, should_reset_task: bool = False):
        raise NotImplementedError()

from collections import namedtuple

Task = namedtuple('Task', ['idempotency_key', 'task_info', 'state'])

TASK_INIT = 'init'
TASK_PENDING = 'pending'
TASK_FAILED = 'failed'
TASK_SUCCEEDED = 'succeeded'


class TaskQueue:
    def enqueue(self, task: Task):
        raise NotImplementedError()

    def dequeue(self) -> Task:
        raise NotImplementedError()

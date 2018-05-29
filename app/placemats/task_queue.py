class TaskQueue:
    def enqueue(self, idemp_key, task_info):
        raise NotImplementedError()

    def dequeue(self):
        raise NotImplementedError()

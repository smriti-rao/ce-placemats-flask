class BaseCache:
    def get(self, key=None):
        raise NotImplementedError()

    def set(self, key=None, data=None, ttl=None):
        raise NotImplementedError()

class BaseStore:
    def get(self, pk=None, pks=None, projection=None, skip=0, limit=0):
        raise NotImplementedError()

    def add(self, to_add, pk=None):
        raise NotImplementedError()

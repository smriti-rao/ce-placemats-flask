class BaseStore:
    def get(self, pk=None, pks=None, projection=None):
        raise NotImplementedError()

    def add(self, to_add, pk=None):
        raise NotImplementedError()

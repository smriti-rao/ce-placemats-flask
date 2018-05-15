class BaseApi:
    def get(self, pk=None):
        if pk is None:
            return self.get_list()
        return self.get_one(pk)

    def get_one(self, pk):
        raise NotImplementedError()

    def get_list(self):
        raise NotImplementedError()

from flask import request


class BaseApi:
    LIMIT_MAX = 20

    def get(self, pk=None):
        if pk is None:
            skip = self.get_query_or_default('skip', 0)
            limit = self.get_query_or_default('limit', self.LIMIT_MAX)
            skip = int(skip)
            limit = min(int(limit), self.LIMIT_MAX)
            return self.get_list(skip=skip, limit=limit)
        return self.get_one(pk)

    def get_one(self, pk):
        raise NotImplementedError()

    def get_list(self, skip=None, limit=None):
        raise NotImplementedError()


    def get_query_or_default(self, query_key, default):
        q = request.args.get(query_key)
        return q if q is not None and q != '' else default

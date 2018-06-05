from typing import Tuple


class BaseStore:
    def get(self, pk=None, pks=None, projection=None, skip=0, limit=0):
        raise NotImplementedError()

    def add(self, to_add, pk=None) -> Tuple[bool, dict]:
        raise NotImplementedError()

    def update(self, pk: str, change_dict: dict):
        raise NotImplementedError()

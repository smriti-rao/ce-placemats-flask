from flask.views import MethodView
from app.placemats.store_config import get_store
from app.placemats.base_api import BaseApi
import logging

logger = logging.getLogger(__name__)


class LayoutsApi(MethodView, BaseApi):
    def get_one(self, pk):
        pk = LayoutsApi._normalize_pk(pk)
        layouts_store = get_store('layouts')
        layout = layouts_store.get(pk=pk)
        if layout is not None:
            return layout
        is_new, layout = layouts_store.add({}, pk=pk)
        if not is_new:
            return layout
        # TODO post-creation logic
        return layout

    def get_list(self):
        return get_store('layouts').get()

    @staticmethod
    def _normalize_pk(pk: str):
        return pk.strip().lower()

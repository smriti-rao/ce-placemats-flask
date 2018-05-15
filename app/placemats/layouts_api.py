from flask.views import MethodView
from app.placemats.store_config import layouts_store
from app.placemats.base_api import BaseApi
import logging

logger = logging.getLogger(__name__)


class LayoutsApi(MethodView, BaseApi):
    def get_one(self, pk):
        pk = LayoutsApi._normalize_pk(pk)
        store = layouts_store()
        layout = store.get(pk=pk)
        if layout is not None:
            return layout
        is_new, layout = store.add({}, pk=pk)
        if not is_new:
            return layout
        # TODO post-creation logic
        return layout

    def get_list(self):
        return layouts_store().get()

    @staticmethod
    def _normalize_pk(pk: str):
        return pk.strip().lower()

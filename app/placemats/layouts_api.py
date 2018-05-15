from flask.views import MethodView
from app.placemats.store import BaseStore
from app.placemats.store_config import get_store
import logging

logger = logging.getLogger(__name__)


class LayoutsApi(MethodView):
    @staticmethod
    def get(pk=None):
        pk = LayoutsApi._normalize_pk(pk)
        layouts_store: BaseStore = get_store('layouts')
        if pk is None:
            return layouts_store.get()
        layout = layouts_store.get(pk=pk)
        if layout is not None:
            return layout
        is_new, layout = layouts_store.add({}, pk=pk)
        if not is_new:
            return layout
        # TODO post-creation logic
        return layout

    @staticmethod
    def _normalize_pk(pk: str):
        return pk.strip().lower() if isinstance(pk, str) else None
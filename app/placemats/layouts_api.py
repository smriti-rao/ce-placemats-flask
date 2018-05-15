from flask.views import MethodView
from app.placemats.store import BaseStore
from app.placemats.store_config import get_store
import logging

logger = logging.getLogger(__name__)


class LayoutsApi(MethodView):
    layouts_store: BaseStore = get_store('layouts')

    def __init__(self) -> None:
        super().__init__()

    def get(self, pk=None):
        if pk is None:
            return self.layouts_store.get()
        layout = self.layouts_store.get(pk=pk)
        if layout is not None:
            return layout
        is_new, layout = self.layouts_store.add({}, pk=pk)
        if not is_new:
            return layout
        # TODO post-creation logic
        return layout

from flask.views import MethodView
from app.placemats.store_config import layouts_store, widgets_store
from app.placemats.store import BaseStore
from app.placemats.base_api import BaseApi
from app.placemats.mock_widget_generator import generate_mock_widgets
import logging

logger = logging.getLogger(__name__)

projected_widget_fields = ['type', 'status', 'href', 'name', 'description']


class LayoutsApi(MethodView, BaseApi):
    LIMIT_MAX = 50

    def get_one(self, pk):
        pk = LayoutsApi._normalize_pk(pk)
        l_store = layouts_store()
        w_store = widgets_store()
        layout = l_store.get(pk=pk)
        if layout is not None:
            return LayoutsApi._resolve_widgets(layout, w_store)
        widgets = generate_mock_widgets()
        w_pks = [w_store.add(w)[1]['_id'] for w in widgets]
        is_new, layout = l_store.add({  # TODO: handle when is_new is False
            'search_terms': pk,
            'widgets': w_pks
        }, pk=pk)
        return LayoutsApi._resolve_widgets(layout, w_store)

    def get_list(self, skip=None, limit=None):
        w_store = widgets_store()
        return [LayoutsApi._resolve_widgets(x, w_store) for x in layouts_store().get(skip=skip, limit=limit)]

    @staticmethod
    def _resolve_widgets(layout, w_store: BaseStore):
        layout['widgets'] = w_store.get(pks=layout['widgets'], projection=projected_widget_fields)
        return layout

    @staticmethod
    def _normalize_pk(pk: str):
        return pk.strip().lower()

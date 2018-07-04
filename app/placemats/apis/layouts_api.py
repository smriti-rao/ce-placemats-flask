from flask.views import MethodView
from app.placemats.stores.store_config import layouts_store, widgets_store
from app.placemats.stores.store import BaseStore
from app.placemats.apis.base_api import BaseApi
from app.placemats.data.widget_spec import widget_specs_for_term
from app.placemats.stores.task_queue_config import widgets_task_queue
from app.placemats.data.auth0_validator import requires_auth
import logging

logger = logging.getLogger(__name__)

projected_widget_fields = ['type', 'status', 'href', 'name', 'description']

STATUS_LOADING = 'loading'
STATUS_COMPLETE = 'complete'


class LayoutsApi(MethodView, BaseApi):
    LIMIT_MAX = 50

    @requires_auth
    def get_one(self, pk: str):
        refresh = self.get_query_or_default('refresh', 0)
        refresh = int(refresh)
        pk = LayoutsApi._normalize_pk(pk)
        l_store = layouts_store()
        w_store = widgets_store()
        layout = l_store.get(pk=pk)
        if layout is not None and refresh == 0:
            return LayoutsApi._resolve_widgets(layout, w_store)
        q = widgets_task_queue()
        w_pks = []
        for spec in widget_specs_for_term(pk):
            is_new, new_widget = w_store.add({
                'type': spec.widget_type,
                'spec_type': spec.spec_type,
                'name': spec.name,
                'description': spec.description,
                'idempotency_key': spec.idempotency_key,
                'status': STATUS_LOADING,
            }, pk=spec.idempotency_key)
            w_pks.append(new_widget['_id'])
            q.enqueue(spec.idempotency_key, spec._asdict())
        if layout is not None and refresh == 1:
            is_update = l_store.update(pk, {'widgets': w_pks})
            layout = l_store.get(pk=pk)
        else:
            is_new, layout = l_store.add({
                'search_terms': pk,
                'widgets': w_pks,
            }, pk=pk)
        return LayoutsApi._resolve_widgets(layout, w_store)

    @requires_auth
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

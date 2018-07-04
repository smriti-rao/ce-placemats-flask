from flask.views import MethodView
from app.placemats.data.auth0_validator import requires_auth
from app.placemats.stores.store_config import widgets_store
from app.placemats.apis.base_api import BaseApi
from flask import abort


class WidgetsApi(MethodView, BaseApi):
    LIMIT_MAX = 10

    @requires_auth
    def get_one(self, pk):
        store = widgets_store()
        widget = store.get(pk=pk)
        if widget is not None:
            return widget
        abort(404)

    @requires_auth
    def get_list(self, skip=None, limit=None):
        return widgets_store().get(skip=skip, limit=limit)

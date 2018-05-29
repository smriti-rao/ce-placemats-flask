from flask.views import MethodView
from app.placemats.store_config import widgets_store
from app.placemats.base_api import BaseApi
from flask import abort


class WidgetsApi(MethodView, BaseApi):
    LIMIT_MAX = 10

    def get_one(self, pk):
        store = widgets_store()
        widget = store.get(pk=pk)
        if widget is not None:
            return widget
        abort(404)

    def get_list(self, skip=None, limit=None):
        return widgets_store().get(skip=skip, limit=limit)

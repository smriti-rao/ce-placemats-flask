from flask.views import MethodView
from flask import jsonify


class PlacematsApi(MethodView):
    def get(self):
        return jsonify(hello='world')

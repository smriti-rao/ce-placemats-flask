from flask.views import MethodView
from flask import jsonify
from app.placemats.ncbi_client import egquery


class PlacematsApi(MethodView):
    def get(self):
        return jsonify(egquery(term='orchid'))

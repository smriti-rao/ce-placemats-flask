import os
import logging

if os.environ.get('FLASK_ENV') == 'development':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger import swagger
from app.placemats.apis.url_config import configure_routes
import app.placemats.data.ncbi_client as ncbi
from app.placemats.util import kwargs_from_environ
from app.placemats.data.auth_error import AuthError


def apply_cors(flask_app):
    CORS(flask_app)
    return flask_app


ncbi.configure_client(**kwargs_from_environ({
    'NCBI_EMAIL': 'email',
    'NCBI_API_KEY': 'api_key',
}))

app = configure_routes(apply_cors(Flask(__name__)))


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route('/swagger')
def swagger_spec():
    return jsonify(swagger(app))


logger.info('Ready')

import os
import logging

if os.environ.get('FLASK_ENV') == 'development':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from flask import Flask, jsonify
from flask_swagger import swagger
from app.placemats.url_config import configure_routes
import app.placemats.ncbi_client as ncbi


def kwargs_from_environ(environ_to_kwarg):
    """
    Adds environment variables to a client kwargs dict that's used to
    configure the biopython ncbi client.
    :param environ_to_kwarg:
    """
    env_keys = filter(lambda k: k in os.environ, environ_to_kwarg.keys())
    return {environ_to_kwarg[k]: os.environ[k] for k in env_keys}


ncbi.configure_client(**kwargs_from_environ({
    'NCBI_EMAIL': 'email',
    'NCBI_API_KEY': 'api_key',
}))

app = configure_routes(Flask(__name__))


@app.route('/swagger')
def swagger_spec():
    return jsonify(swagger(app))


logger.info('Ready')

from flask import Flask, jsonify
from flask_swagger import swagger
from app.placemats.url_config import configure_routes
import app.placemats.ncbi_client as ncbi
import os


def kwargs_from_environ(environ_to_kwarg):
    """
    Adds environment variables to a client kwargs dict that's used to
    configure the biopython ncbi client.
    :param environ_to_kwarg:
    """
    out = {}
    for environ_key, kwarg_key in environ_to_kwarg.items():
        if os.environ.get(environ_key):
            out[kwarg_key] = os.environ[environ_key]
    return out


ncbi.configure_client(kwargs_from_environ({
    'NCBI_EMAIL': 'email',
    'NCBI_API_KEY': 'api_key',
}))

app = configure_routes(Flask(__name__))


@app.route('/swagger')
def swagger_spec():
    return jsonify(swagger(app))

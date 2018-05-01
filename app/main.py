from flask import Flask, jsonify
from flask_swagger import swagger
from app.placemats.url_config import configure_routes

app = configure_routes(Flask(__name__))


@app.route('/swagger')
def swagger_spec():
    return jsonify(swagger(app))


@app.route('/health')
def health_check():
    return jsonify(is_healthy=True)

from functools import wraps
from flask import jsonify


def jsonify_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return jsonify(f(*args, **kwargs))

    return decorated_function

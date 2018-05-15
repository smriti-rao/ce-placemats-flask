from app.placemats.api import PlacematsApi
from app.placemats.layouts_api import LayoutsApi
from app.placemats.decorators import jsonify_view


def register_api(app, view, endpoint, url, pk_type='string'):
    pk = 'pk'
    """
    reference: http://flask.pocoo.org/docs/0.12/views/#method-views-for-apis
    """
    view_func = jsonify_view(view.as_view(endpoint))
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def configure_routes(app):
    register_api(app, LayoutsApi, endpoint='layouts_resource', url='/layouts/')
    # register_api(app, PlacematsApi, endpoint='placemats_api', url='/placemats/', pk='search_terms')
    return app

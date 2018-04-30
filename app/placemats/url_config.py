from app.placemats.api import PlacematsApi


def configure_routes(app):
    app.add_url_rule('/placemats', view_func=PlacematsApi.as_view('placemats'))
    return app

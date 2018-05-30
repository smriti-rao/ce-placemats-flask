from app.placemats.stores.mongo_cache import MongoCache
from app.placemats.stores.mongo_client import mongo_db


def widgets_cache():
    return MongoCache(mongo_db()['widgets_cache'], ttl=43_200)

import os
import pymongo


def mongo_db():
    if 'MONGO_URL' in os.environ:
        url = os.environ['MONGO_URL']
    else:
        url = 'mongodb://127.0.0.1:27017/'
    return pymongo.MongoClient(url)['placemats']

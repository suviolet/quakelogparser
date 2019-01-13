from pymongo import MongoClient as client

from core.settings import (MONGODB_COLLECTION, MONGODB_DB, MONGODB_PORT,
                           MONGODB_SERVER)


class MongoClient(object):

    collection_name = MONGODB_COLLECTION

    def __init__(self):
        self.mongo_uri = MONGODB_SERVER
        self.mongo_db = MONGODB_DB
        self.mongo_port = MONGODB_PORT
        self.client = client(self.mongo_uri, self.mongo_port)

        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

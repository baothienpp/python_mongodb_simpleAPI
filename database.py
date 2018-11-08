from pymongo import MongoClient


class Database():
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client['data']
        self.conf = db['configuration']

    def push(self, data):
        # User could post many docs, insert_one will block
        # Maybe a buffer ? asynchro io ?
        self.conf.insert_one(data)

    def query(self, tenant=None, integration_type=None):
        self.conf.find({'tenant': tenant, 'integration_type': integration_type})

    def update(self):
        pass


print('s')

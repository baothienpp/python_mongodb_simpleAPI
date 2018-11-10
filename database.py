from pymongo import MongoClient


class Database:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client['data']
        self.conf = db['configuration']

    async def push(self, data):
        result = self.conf.insert_one(data)

        if result.inserted_id:
            return True
        else:
            return False

    async def query(self, tenant=None, integration_type=None):
        query = {'tenant': tenant, 'integration_type': integration_type}
        query = {k: v for k, v in query.items() if v is not None}

        result = []
        for doc in self.conf.find(query):
            doc.pop('_id')
            result.append(doc)

        return result

    def update(self):
        pass



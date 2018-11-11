from pymongo import MongoClient, ReturnDocument


class Database:
    def __init__(self, address, database, collection):
        client = MongoClient(address, 27017)
        db = client[database]
        self.conf = db[collection]

    async def push(self, data):
        """
        Create document in a collection. Exist
        :param data:
        :return:
        """
        query = {k: data.get(k) for k in ('tenant', 'integration_type')}

        status = self.conf.find_one_and_update(filter=query,
                                               update={'$set': {'configuration': data.get('configuration')}},
                                               return_document=ReturnDocument.AFTER)
        if status is None:
            status = self.conf.insert_one(data)

        return status

    async def query(self, tenant=None, integration_type=None):
        """

        :param tenant:
        :param integration_type:
        :return:
        """
        query = {'tenant': tenant, 'integration_type': integration_type}
        query = {k: v for k, v in query.items() if v is not None}

        result = []
        for doc in self.conf.find(query):
            doc.pop('_id')
            result.append(doc)

        return result

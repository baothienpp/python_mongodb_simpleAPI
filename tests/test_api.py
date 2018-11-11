import pytest
import asynctest
from pymongo import MongoClient
import json
from ..api import app
from ..database import Database


class TestAPI(asynctest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['database'] = Database('localhost', 'data', 'test')

        db_client = MongoClient('localhost', 27017)
        _db = db_client['data']
        self.conf = _db['test']

    @pytest.mark.asyncio
    async def test_app_get(self):
        self.conf.delete_many({})

        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})

        data_tmp = {}
        data_tmp.update(data)
        self.conf.insert_one(data_tmp)

        response = await self.client.get('/config')
        content = await response.get_data()
        content = content.decode("utf-8")

        assert content == json.dumps(data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_app_post(self):
        self.conf.delete_many({})

        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})

        response = await self.client.post('/config', json=data)

        result = []
        for doc in self.conf.find({'tenant': 'user1', 'integration_type': 'booking'}):
            doc.pop('_id')
            result.append(doc)

        assert result[0] == data
        assert response.status_code == 201

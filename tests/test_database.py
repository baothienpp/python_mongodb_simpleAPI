from pymongo import MongoClient
import pytest
import asynctest

from ..database import Database


class TestDatabase(asynctest.TestCase):
    def setUp(self):
        self.database = Database('localhost', 'data', 'test')

        client = MongoClient('localhost', 27017)
        _db = client['data']
        self.conf = _db['test']

    @pytest.mark.asyncio
    async def test_push_new(self):
        self.conf.delete_many({})
        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})
        status = await self.database.push(data)
        assert status

        for doc in self.conf.find({'tenant': 'user1',
                                   'integration_type': 'booking'}):
            assert doc == data

    @pytest.mark.asyncio
    async def test_push_update(self):
        self.conf.delete_many({})
        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})
        await self.database.push(data)

        update_data = dict({'tenant': 'user1',
                            'integration_type': 'booking',
                            'configuration': {'test_conf2': '2'}})

        await self.database.push(update_data)

        for doc in self.conf.find({'tenant': 'user1',
                                   'integration_type': 'booking'}):
            doc.pop('_id')
            assert doc == update_data

    @pytest.mark.asyncio
    async def test_query(self):
        self.conf.delete_many({})
        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})
        data_tmp = {}
        data_tmp.update(data)

        self.conf.insert_one(data_tmp)

        result = await self.database.query(tenant='user1')

        assert result[0] == data

    @pytest.mark.asyncio
    async def test_query_not_found(self):
        self.conf.delete_many({})
        data = dict({'tenant': 'user1',
                     'integration_type': 'booking',
                     'configuration': {'test_conf1': '1'}})
        data_tmp = {}
        data_tmp.update(data)

        self.conf.insert_one(data_tmp)

        result = await self.database.query(tenant='user1', integration_type='booking2')

        self.assertFalse(result)

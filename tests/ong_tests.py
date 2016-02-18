# coding: utf-8

import unittest
import json
from app import app
from ong.documents import OngDocument


class OngTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        OngDocument.drop_collection()

    def test_post_ong(self):
        ong = {'name': 'Expresso Voluntário', 'description': 'Unindo ONGs e voluntários'}
        response = self.client.post('/ong/', data=ong)
        # response_data_decoded = response.data.decode()
        self.assertEquals(response.status_code, 201)

    def test_post_ong_without_required_parameters(self):
        ong = {'description': 'Unindo ONGs e voluntários'}
        response = self.client.post('/ong/', data=ong)
        # response_data_decoded = response.data.decode()
        self.assertEquals(response.status_code, 400)

    def test_get_ong(self):
        ong = OngDocument(name='Expresso Voluntário', description='Unindo ONGs e voluntários').save()
        response = self.client.get('/ong/{id}'.format(id=ong.id))
        response_data_decoded = response.data.decode()
        ong_response = json.loads(response_data_decoded)
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(ong.to_dict(), ong_response)

    def test_get_ong_nonexistent(self):
        response = self.client.get('/ong/{id}'.format(id="fake_id"))
        self.assertEquals(response.status_code, 404)

    def test_get_ong_without_pass_id_and_limit(self):
        response = self.client.get('/ong/')
        self.assertEquals(response.status_code, 400)

    def test_get_all_ongs(self):
        OngDocument(name='Expresso Voluntário', description='Unindo ONGs e voluntários').save()
        response = self.client.get('/ong/', data={'limit': 10})
        response_data_decoded = response.data.decode()
        ongs = json.loads(response_data_decoded)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(ongs), 1)

    def test_delete_ong(self):
        ong = OngDocument(name='Expresso Voluntário', description='Unindo ONGs e voluntários').save()
        response = self.client.delete('/ong/{id}'.format(id=ong.id))
        self.assertEquals(response.status_code, 204)

    def test_delete_ong_nonexistent(self):
        response = self.client.delete('/ong/{id}'.format(id='fake_id'))
        self.assertEquals(response.status_code, 404)

    def test_delete_ong_without_pass_id(self):
        response = self.client.delete('/ong/')
        self.assertEquals(response.status_code, 400)

    def test_put_ong(self):
        ong = {'name': 'Expresso Voluntário', 'description': 'Unindo ONGs e voluntários'}
        response = self.client.post('/ong/', data=ong)
        data_decoded_1 = response.data.decode()
        self.assertEquals(response.status_code, 201)

        ong_modified = json.loads(data_decoded_1)
        ong_modified['name'] = 'Expresso Voluntário Modified'
        _id = ong_modified['id']
        del ong_modified['id']
        response_2 = self.client.put('/ong/{id}'.format(id=_id), data=ong_modified)
        data_decoded_2 = response_2.data.decode()
        self.assertEquals(response_2.status_code, 201)

        ong1 = json.loads(data_decoded_1)
        ong2 = json.loads(data_decoded_2)
        self.assertNotEquals(ong1['name'], ong2['name'])

    def test_put_ong_nonexistent_id(self):
        ong = {'name': 'Expresso Voluntário', 'description': 'Unindo ONGs e voluntários'}
        response = self.client.put('/ong/{id}'.format(id='fake_id'), data=json.dumps(ong))
        self.assertEquals(response.status_code, 404)

    def test_put_ong_without_pass_id(self):
        ong = {'name': 'Expresso Voluntário', 'description': 'Unindo ONGs e voluntários'}
        response = self.client.put('/ong/', data=json.dumps(ong))
        self.assertEquals(response.status_code, 400)

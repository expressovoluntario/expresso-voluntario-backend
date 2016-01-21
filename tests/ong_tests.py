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
        ong = {'name': 'Expresso Voluntário', 'description': 'Description'}
        response = self.client.post('/ong/', data=ong)
        response_data_decoded = response.data.decode()
        ongResponse = json.loads(response_data_decoded)

        self.assertEquals(response.status_code, 201)
        #  self.assertDictContains(ong, ongResponse)

    def test_get_ong(self):
        ong = OngDocument(name='ONG 1', description='Lorem Ipsum').save()

        response = self.client.get('/ong/{id}'.format(id=ong.id))
        response_data_decoded = response.data.decode()
        ong_response = json.loads(response_data_decoded)
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(ong.to_dict(), ong_response)

    def test_get_all_ongs(self):
        OngDocument(name='ONG 1', description='Lorem Ipsum').save()
        response = self.client.get('/ong/', data={'limit': 10})
        response_data_decoded = response.data.decode()
        ongs = json.loads(response_data_decoded)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(ongs), 1)

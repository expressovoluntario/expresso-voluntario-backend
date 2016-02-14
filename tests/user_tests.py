import json
import unittest
from flask.ext.login import current_user, login_user
from app import app
from user.documents import UserDocument
from ong.documents import OngDocument


class UserTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.user = UserDocument(name="iury", email="iury@gmail.com", _password="blabla").save()
        self.ong = OngDocument(name='ong', description='The coolest ong').save()

    def tearDown(self):
        UserDocument.drop_collection()
        OngDocument.drop_collection()

    def test_get_one_user(self):
        response = self.client.get("/user/{id}".format(id=self.user.id))
        decoded_response = json.loads(response.data.decode())

        self.assertEquals(decoded_response, self.user.to_dict())

    def test_get_inexistent_user(self):
        id_ = '123abc'
        response = self.client.get("/user/{id}".format(id=id_))

        self.assertEquals(response.status_code, 404)

    def test_get_many_users(self):
        UserDocument(name='willian', email='william@ribeiro.com', _password='willfix').save()
        limit = 10
        response = self.client.get("/user/?limit={limit}".format(limit=limit))
        decoded_response = json.loads(response.data.decode())

        self.assertEqual(len(decoded_response), 2)
        self.assertEqual(response.status_code, 200)

    def test_malformed_user_request(self):
        response = self.client.get("/user/")
        decoded_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(decoded_response, {'message': 'You must provide limit or id'})

    def test_add_user(self):
        data = {
            'name': 'travis',
            'email': 'travis@travis.com',
            'password': 'travis',
            'ong_id': self.ong.id
        }
        response = self.client.post("/user/", data=data)
        saved_user = UserDocument.objects.get(email='travis@travis.com')
        decoded_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(decoded_response, saved_user.to_dict())

    def test_delete_user(self):
        id_ = self.user.id
        response = self.client.delete('/user/{id}'.format(id=id_))

        self.assertEqual(response.status_code, 204)

    def test_delete_user_insufficient_params(self):
        response = self.client.delete('/user/')
        decoded_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(decoded_response, {"message": "You must provide an id"})

    def test_put_user_insufficient_params(self):
        response = self.client.put('/user/')
        decoded_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(decoded_response, {"message": "You must provide an id"})

    def test_put_user(self):
        data = {"name": "newname", "email": "new@email.com"}
        response = self.client.put('/user/{id}'.format(id=self.user.id), data=data)
        user = UserDocument.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.email, data['email'])

    def test_put_not_found_user(self):
        response = self.client.put("/user/1012")

        self.assertEqual(response.status_code, 404)


class LoginTests(unittest.TestCase):

    def setUp(self):
        UserDocument.drop_collection()
        self.user = UserDocument(name="iury", email="iury@gmail.com", _password="blabla").save()

    def tearDown(self):
        UserDocument.drop_collection()

    def test_login_success(self):
        data = {"email": self.user.email, "password": 'blabla'}
        with app.test_request_context(), app.test_client() as client:
            response = client.get('/user/login/', data=data)

            self.assertEquals(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)

    def test_login_wrong_password(self):
        data = {"email": self.user.email, "password": "vampeta"}
        with app.test_request_context(), app.test_client() as client:
            response = client.get("/user/login/", data=data)

            self.assertEqual(response.status_code, 401)
            self.assertFalse(current_user.is_authenticated)

    def test_login_user_not_found(self):
        data = {"email": "olololo@age.com", "password": "blabla"}
        with app.test_request_context(), app.test_client() as client:
            response = client.get("/user/login/", data=data)

            self.assertEqual(response.status_code, 401)
            self.assertFalse(current_user.is_authenticated)


class LogoutTests(unittest.TestCase):

    def setUp(self):
        self.user = UserDocument(name="iury", email="iury@gmail.com", _password="blabla").save()

    def tearDown(self):
        UserDocument.drop_collection()

    def test_logout(self):
        with app.test_request_context(), app.test_client() as client:
            login_user(self.user)
            response = client.get("/user/logout/")

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)

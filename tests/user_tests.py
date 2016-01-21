import unittest
from app import app
from user.documents import UserDocument

class LoginTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.user = UserDocument(name="iury", email="iury@gmail.com", _password="blabla").save()

    def tearDown(self):
        UserDocument.drop_collection()

    def test_login(self):
        data = {"email": self.user.email, "password": 'blabla'}
        response = self.client.get('/user/login/', data=data)

        self.assertEquals(response.status_code, 200)

    def test_login_wrong_password(self):
        data = {"email": self.user.email, "password": "vampeta"}
        response = self.client.get("/user/login/", data=data)

        self.assertEqual(response.status_code, 401)

    def test_login_user_not_found(self):
        data = {"email": "olololo@age.com", "password": "blabla"}
        response = self.client.get("/user/login/", data=data)

        self.assertEqual(response.status_code, 401)
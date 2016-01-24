import unittest
from flask.ext.login import current_user, login_user
from app import app
from user.documents import UserDocument


class LoginTests(unittest.TestCase):

    def setUp(self):
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

import os
import unittest
from urllib.parse import urlparse

from flask_login import current_user

from tea_site import create_app, db
from tea_site.models import *
from tea_site.config import TestConfig

app = create_app(config=TestConfig)

with app.app_context():
    db.drop_all()
    db.create_all()


class UsersRouteBasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_login_page(self):
        response = self.app.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get("/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_account_page(self):
        response = self.app.get("/account", follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class UsersRegisterTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, email, password):
        return self.app.post(
            "/login", data=dict(email=email, password=password), follow_redirects=True
        )

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def register(self, email, fname, lname, password):
        return self.app.post(
            "/register",
            data=dict(
                email=email,
                first_name=fname,
                last_name=lname,
                password=password,
                confirm_password=password,
            ),
            follow_redirects=True,
        )

    def test_login(self):
        r = self.login("test@test.com", "12345678")
        self.assertTrue("Вход не удался" in r.data.decode("utf-8"))
        r = self.register("test@test.com", "Test", "Test", "12345678")
        self.assertTrue("Аккаунт был успешно создан" in r.data.decode("utf-8"))
        r = self.login("test@test.com", "12345678")
        self.assertTrue("Вы успешно вошли в аккаунт" in r.data.decode("utf-8"))
        r = self.logout()
        self.assertTrue("Вы вышли из аккаунта" in r.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()

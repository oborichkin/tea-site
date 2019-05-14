import os
import unittest

from tea_site import create_app
from tea_site.config import TestConfig

app = create_app(config=TestConfig)


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_home_page(self):
        response = self.app.get("/home", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get("/about", follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

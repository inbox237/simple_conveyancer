import unittest
from flask import Flask
from main import create_app, db

class TestAlbums(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])
        print("setup ran")

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_album_index(self):
        response = self.client.get("/albums/")

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
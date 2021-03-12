import unittest
import os
from models.Settlement import Settlement
from models.User import User
from main import create_app, db

class TestSettlements(unittest.TestCase):
    #Runs before the tests
    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV is not testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    #GET method in /settlements/
    def test_settlement_index(self):
        response = self.client.post('/auth/login', data={
            'username': 'testusername1',
            'password': '1234'
        }, follow_redirects=True)

        #print(response.data)
        self.assertEqual(response.status_code, 200)

        #response is going to contain the html with all the settlements
        response = self.client.get("/settlements/")

        #get all the settlements from the database
        user = User.query.first()
        #print(settlements[0].city)
        self.assertEqual(response.status_code, 200)
        #test if we have the title of the html in the content of the response
        self.assertIn("Settlements", str(response.data))
        #test content from the layout

        #test if the html contains the names and cities of the settlements
        self.assertIn(user.user_s_settlements[0].name, str(response.data))
        self.assertIn(user.user_s_settlements[1].name, str(response.data))

    def test_settlement_by_id(self):
        response = self.client.get(f"/settlements/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("My Settlements", str(response.data))

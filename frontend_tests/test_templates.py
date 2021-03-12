import unittest
import os
from models.Settlement import Settlement
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
        runner.invoke(args=["db", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    #GET method in /settlements/
    def test_settlement_index(self):
        #response is going to contain the html with all the settlements
        response = self.client.get("/settlements/")
        #print(response.data)
        #get all the settlements from the database
        settlements = Settlement.query.all()
        #print(settlements[0].city)
        self.assertEqual(response.status_code, 200)
        #test if we have the title of the html in the content of the response
        self.assertIn("Settlements", str(response.data))
        #test content from the layout

        self.assertIn("Welcome", str(response.data))
        #test if the html contains the names and cities of the settlements
        self.assertIn(settlements[0].name, str(response.data))
        self.assertIn(settlements[1].name, str(response.data))

    def test_settlement_by_id(self):
        settlement = Settlement.query.first()
        response = self.client.get(f"/settlements/{settlement.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Name", str(response.data))
        self.assertIn(settlement.name, str(response.data))
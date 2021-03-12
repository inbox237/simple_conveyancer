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

    #POST method in settlements
    def test_post_settlement_create(self):
        #register and login a user
        response = self.client.post('/auth/register', data={
            'username': 'tester',
            'password': '123456'
        })
        #print(response.data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/auth/login', data={
            'username': 'tester',
            'password': '123456'
        }, follow_redirects=True)

        #print(response.data)
        self.assertEqual(response.status_code, 200)

        #creating the data for the settlement
        settlement_data = {
            "name": "unittest_name",
            "settdate": "2021-06-06",
            "address": "unittest_address",
            "saleprice": "7777",
            "deposit": "777",
            "ratesamount": "77",
            "ratesstatus": "on",
            "balance": "77",
            "ratesdayspaid": "77",
            "ratesdaysunpaid": "77",
            "ratesoverpaid": "77",
            "ratesunderpaid": "77",
            "totalbalance": "55",
        }

        response = self.client.post("settlements/",data = settlement_data)
        settlement = self.client.get("settlements/")
        self.assertIsNotNone(settlement)
        self.assertIn("unittest_name", str(settlement.data))


    # test the GET method in /settlements/ returns all the settlements
    def test_get_all_settlements(self):
        response = self.client.get("/settlements/")
        #data = response.get_json()
        
        #check the OK status
        self.assertEqual(response.status_code, 200)
        #Check that we receive a string in the html response
        self.assertIn("Settlements", str(response.data))

    

    # # #DELETE method in settlements/id, not allowed to delete
    # def test_delete_settlement_not_allowed(self):
    #     #register and login a user
    #     response = self.client.post('/auth/register', data={
    #         'username': 'tester',
    #         'password': '123456'
    #     })
        
    #     self.assertEqual(response.status_code, 302)
    #     response = self.client.post('/auth/login', data={
    #         'username': 'tester',
    #         'password': '123456'
    #     }, follow_redirects=True)
        
    #     self.assertEqual(response.status_code, 200)
    #     #get the first settlement

    #     settlement = Settlement.query.first()
    #     #try to delete it

    #     response = self.client.get(f"/settlements/delete/{settlement.id}")
    #     #test a 400 status, a user is not the owner of the settlement cannot delete it
    #     self.assertEqual(response.status_code, 400)

    # # #DELETE method on /settlements/id allowed
    # def test_delete_settlement_allowed(self):
    #     #login a user that already exists and get the token
    #     #login the user that already owns a settlement
    #     response = self.client.post('/auth/login', data={
    #         'username': 'testusername1',
    #         'password': '1234'
    #     }, follow_redirects=True)
    #     #print(response.data)
    #     self.assertEqual(response.status_code, 200)

    #     settlement = Settlement.query.first()
    #     response = self.client.get(f"settlements/delete/{settlement.id}")
    #     #test the OK status
    #     self.assertEqual(response.status_code, 200)
    #     #query to the settlement we deleted
    #     settlement_del = Settlement.query.get(settlement.id)
    #     #test that none has been received
    #     self.assertIsNone(settlement_del)



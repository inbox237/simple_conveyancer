from main import db
from flask import Blueprint, Flask
import click
from click import pass_context
import webbrowser
import os

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Settlement import Settlement
     
    from main import bcrypt
    from faker import Faker
    import random
    faker = Faker()


#Initial Setup
    users = []

    #Users/Settlements
    for i in range(1,5):
        user = User()
        settlement = Settlement()

        user.username = f"testusername{i}"
        user.password = bcrypt.generate_password_hash("1234").decode("utf-8")

        settlement.user_id = faker.random_int(min=1, max=4)
        settlement.name = f"testsettlementname{i}"
        settlement.saleprice = faker.random_int(min=300000, max=1000000)
        settlement.deposit = faker.random_int(min=15000, max=20000)
        settlement.settdate = "2021-06-06"


        print(f"{i} Users & Settlements Created")
        db.session.add(user)
        db.session.add(settlement)
        users.append(user)

    db.session.commit()

    print("Tables seeded")


@db_commands.cli.command("start")
@pass_context
def refresh_db(ctx):
    drop_db.invoke(ctx)
    create_db.invoke(ctx)
    seed_db.invoke(ctx)
    print("All Done!, Flask program will now start....")
    webbrowser.open("http://127.0.0.1:5000/signup")
    os.system("flask run")


    
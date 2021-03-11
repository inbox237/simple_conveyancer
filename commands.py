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

    usr_pla_association_pairs = []

    count_pla_usr = [0]*10
    count_usr_pla = [0]*10


    #Users/Settlements
    for i in range(1,11):
        user = User()
        settlement = Settlement()
        user.username = f"testusername{i}"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")

    
        db.session.add(user)
        db.session.add(settlement)
        users.append(user)

    db.session.commit()


#FINAL COUNTS

    #Count User's settlements
    print(f'usr_count: {count_usr_pla}')
    for i,val in enumerate(count_usr_pla):
        print(f'ind: {i} val: {val}')
        user = db.session.query(User).filter(User.id==i+1).one()
        user.user_s_settlements_count = val
        db.session.commit()

    #Count Settlement's Users
    print(f'pla_count: {count_pla_usr}')
    for i,val in enumerate(count_pla_usr):
        print(f'ind: {i} val: {val}')
        settlement = db.session.query(Settlement).filter(Settlement.id==i+1).one()
        settlement.settlement_s_users_count = val
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


    
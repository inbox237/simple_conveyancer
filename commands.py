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
   
    from models.User_Settlement_Association import user_settlement_association_table as upat
    
    from main import bcrypt
    from faker import Faker
    import random
    faker = Faker()


#Initial Setup
    users = []

    usr_pla_association_pairs = []

    count_pla_usr = [0]*10
    count_usr_pla = [0]*10



#Association Lists SETUP + Counts
    for i in range(1,11):

        usr_int = random.randint(1,10)
        pla_int = random.randint(1,10)
       
        #Append Association List - Users and Settlements - don't enter duplicates
        while (usr_int,pla_int) in usr_pla_association_pairs:
            usr_int = random.randint(1,10)
            pla_int = random.randint(1,10)

        #Add count both directions
        count_usr_pla[usr_int-1]+=1
        count_pla_usr[pla_int-1]+=1

        usr_pla_association_pairs.append((usr_int,pla_int))


    #Users/Settlements
    for i in range(1,11):
        user = User()
        settlement = Settlement()

        settlement.settlement_title = faker.unique.catch_phrase()

        user.email = f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.seasonal_offer = faker.random_int(min=1, max=4)
    
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


    #create association tables
    db.session.execute(upat.insert().values(usr_pla_association_pairs))
    db.session.commit()

    print("Tables seeded")


@db_commands.cli.command("start")
@pass_context
def refresh_db(ctx):
    drop_db.invoke(ctx)
    create_db.invoke(ctx)
    seed_db.invoke(ctx)
    print("All Done!, Flask program will now start....")
    webbrowser.open("http://127.0.0.1:5000/settlements/")
    os.system("flask run")


    
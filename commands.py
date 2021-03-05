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
    from models.Album import Album
    from models.Artist import Artist
    from models.User import User
    from models.Track import Track
    from models.Playlist import Playlist
    from models.SeasonalD import SeasonalD
    from models.Album_Artist_Association import album_artist_association_table as aaat
    from models.User_Playlist_Association import user_playlist_association_table as upat
    
    from main import bcrypt
    from faker import Faker
    import random
    faker = Faker()


#Initial Setup
    users = []

    art_alb_association_pairs = []
    alb_tra_association_pairs = []
    tra_pla_association_pairs = []
    usr_pla_association_pairs = []

    count_art_alb = [0]*10
    count_alb_art = [0]*10

    count_alb_tra = [0]*10
    count_tra_alb = [0]*10

    count_tra_pla = [0]*10
    count_pla_tra = [0]*10

    count_pla_usr = [0]*10
    count_usr_pla = [0]*10




#Association Lists SETUP + Counts
    for i in range(1,11):

        usr_int = random.randint(1,10)
        pla_int = random.randint(1,10)
        art_int = random.randint(1,10)
        alb_int = random.randint(1,10)
        tra_int = random.randint(1,10)

       
        #Append Association List - Albums and Artists - don't enter duplicates
        while (art_int,alb_int) in art_alb_association_pairs:
            art_int = random.randint(1,10)
            alb_int = random.randint(1,10)

        #Append Association List - Users and Playlists - don't enter duplicates
        while (usr_int,pla_int) in usr_pla_association_pairs:
            usr_int = random.randint(1,10)
            pla_int = random.randint(1,10)

        #Add count both directions
        count_usr_pla[usr_int-1]+=1
        count_pla_usr[pla_int-1]+=1

        count_art_alb[art_int-1]+=1
        count_alb_art[alb_int-1]+=1

        art_alb_association_pairs.append((art_int,alb_int))
        usr_pla_association_pairs.append((usr_int,pla_int))


    #Seasonal Discounts
    for i in range(1,5):       
        seasonald = SeasonalD()
        seasonsname = {
        1: "Summer",
        2: "Autumn",
        3: "Spring",
        4: "Winter"}

        seasonsfloat = {
        1: 15.0,
        2: 20.0,
        3: 25.0,
        4: 30.0}

        seasonald.seasonald_title = seasonsname[i]
        seasonald.seasonald_offer = seasonsfloat[i]
        db.session.add(seasonald)
    db.session.commit()

    #Users/Playlists
    for i in range(1,11):
        user = User()
        playlist = Playlist()

        playlist.playlist_title = faker.unique.catch_phrase()

        user.email = f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.seasonal_offer = faker.random_int(min=1, max=4)
    
        db.session.add(user)
        db.session.add(playlist)
        users.append(user)

    db.session.commit()


    #Tracks
    for i in range(1,11):
        track = Track()
        track.track_title = faker.unique.catch_phrase()
        track.track_duration = faker.random_int(min=120, max=480)
        db.session.add(track)
   
    db.session.commit()





    #for i in enumerate(SeasonalD().id):
       # seasonald = SeasonalD()
      #  seasonald.seasonald_title = seasonsname[seasonald.id]
      #  seasonald.seasonald_offer = seasonsfloat[seasonald.id]
      #  db.session.commit()
        
    #playlist = db.session.query(Playlist).filter(Playlist.id==i+1).one()
    #Seasonal Discounts Update!
    #seasonald.seasonald_title = seasonsname[seasonald.id]
    #seasonald.seasonald_offer = seasonsfloat[seasonald.id]
    #db.session.commit()


    #Seasonal Discounts Update!
    #seasonald.seasonald_title = seasonsname[seasonald.id]
    #seasonald.seasonald_offer = seasonsfloat[seasonald.id]
    #db.session.commit()




    #Artists/Albums
    for i in range(1,11):
        artist = Artist()
        album = Album()
        artist.user_id = random.choice(users).id
        artist.artist_name = faker.unique.name()
        album.album_title = faker.unique.catch_phrase()
        
        db.session.add(artist)
        db.session.add(album)
   
    db.session.commit()





#FINAL COUNTS
    #Count Artist's Albums
    print(f'art_count: {count_art_alb}')
    for i,val in enumerate(count_art_alb):
        print(f'ind: {i} val: {val}')
        artist = db.session.query(Artist).filter(Artist.id==i+1).one()
        artist.artist_s_albums_count = val
        db.session.commit()

    #Count Album's Artists
    print(f'alb_count: {count_alb_art}')
    for i,val in enumerate(count_alb_art):
        print(f'ind: {i} val: {val}')
        album = db.session.query(Album).filter(Album.id==i+1).one()
        album.album_s_artists_count = val
        db.session.commit()

    #Count Album's Tracks
    print(f'pla_count: {count_pla_usr}')
    for i,val in enumerate(count_pla_usr):
        print(f'ind: {i} val: {val}')
        playlist = db.session.query(Playlist).filter(Playlist.id==i+1).one()
        playlist.playlist_s_users_count = val
        db.session.commit()

    #Count User's playlists
    print(f'usr_count: {count_usr_pla}')
    for i,val in enumerate(count_usr_pla):
        print(f'ind: {i} val: {val}')
        user = db.session.query(User).filter(User.id==i+1).one()
        user.user_s_playlists_count = val
        db.session.commit()

    #Count Playlist's Users
    print(f'pla_count: {count_pla_usr}')
    for i,val in enumerate(count_pla_usr):
        print(f'ind: {i} val: {val}')
        playlist = db.session.query(Playlist).filter(Playlist.id==i+1).one()
        playlist.playlist_s_users_count = val
        db.session.commit()


    #create association tables
    db.session.execute(aaat.insert().values(art_alb_association_pairs))
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
    webbrowser.open("http://127.0.0.1:5000/artists/")
    os.system("flask run")


    
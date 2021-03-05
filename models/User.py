from main import db

from models.User_Playlist_Association import user_playlist_association_table as upat

from models.Playlist import Playlist

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    user_s_playlists_count = db.Column(db.Integer())
    seasonal_offer = db.Column(db.Integer, db.ForeignKey("seasonalds.id"), nullable=True)
    seasonal_playlists = db.Column(db.Integer, db.ForeignKey("seasonalps.id"), nullable=True)
    user_s_playlists = db.relationship("Playlist", secondary=upat,
                        back_populates="playlist_s_users")

    artists = db.relationship("Artist", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"
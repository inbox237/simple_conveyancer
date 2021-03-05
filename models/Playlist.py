from main import db

from models.Track_Playlist_Association import track_playlist_association_table as tpat
from models.User_Playlist_Association import user_playlist_association_table as upat


class Playlist(db.Model):
    __tablename__ = "playlists"
    
    id = db.Column(db.Integer, primary_key=True)
    playlist_title = db.Column(db.String())
    playlist_s_tracks_count = db.Column(db.Integer())
    playlist_s_users_count = db.Column(db.Integer())
    playlist_s_tracks = db.relationship("Track",
                        secondary=tpat,
                        back_populates="track_s_playlists")
    playlist_s_users = db.relationship("User",
                        secondary=upat,
                        back_populates="user_s_playlists")

    def __repr__(self):
        return f"<Track {self.playlist_title}>"

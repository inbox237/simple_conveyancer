from main import db

from models.Album_Artist_Association import album_artist_association_table as aaat
from models.Album_Track_Association import album_track_association_table as atat

from models.Artist import Artist

class Album(db.Model):
    __tablename__ = "albums"
    
    id = db.Column(db.Integer, primary_key=True)
    album_title = db.Column(db.String())
    album_s_artists_count = db.Column(db.Integer())
    album_s_tracks_count = db.Column(db.Integer())
    album_s_artists = db.relationship("Artist",
                        secondary=aaat,
                        back_populates="artist_s_albums")
    
    album_s_tracks = db.relationship("Track",
                        secondary=atat,
                        back_populates="track_s_albums")

    def __repr__(self):
        return f"<Album {self.album_title}>"

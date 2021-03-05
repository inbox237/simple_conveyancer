from main import db


from models.Album_Track_Association import album_track_association_table as atat
from models.Track_Playlist_Association import track_playlist_association_table as tpat

from models.Album import Album

class Track(db.Model):
    __tablename__ = "tracks"
    
    id = db.Column(db.Integer, primary_key=True)
    track_title = db.Column(db.String())
    track_duration = db.Column(db.Integer())
    track_s_albums_count = db.Column(db.Integer())
    track_s_playlists_count = db.Column(db.Integer())
    track_s_albums = db.relationship("Album",
                        secondary=atat,
                        back_populates="album_s_tracks")
    track_s_playlists = db.relationship("Playlist",
                        secondary=tpat,
                        back_populates="playlist_s_tracks")

    def __repr__(self):
        return f"<Track {self.track_title}>"

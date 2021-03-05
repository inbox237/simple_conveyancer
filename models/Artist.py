from main import db

from models.Album_Artist_Association import album_artist_association_table as aaat



class Artist(db.Model):
    __tablename__ = "artists"
    
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    artist_s_albums_count = db.Column(db.Integer())
    
    artist_s_albums = db.relationship("Album",
                        secondary=aaat,
                        back_populates="album_s_artists")

    def __repr__(self):
        return f"<Artist {self.artist_name}>"
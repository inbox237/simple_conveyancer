from main import db

album_artist_association_table = db.Table("album_artist_association_table", db.Model.metadata,
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"),primary_key=True),
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"), primary_key=True))
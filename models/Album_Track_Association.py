from main import db

album_track_association_table = db.Table("album_track_association_table", db.Model.metadata,
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"),primary_key=True),
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True))
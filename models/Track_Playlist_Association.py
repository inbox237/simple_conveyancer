from main import db

track_playlist_association_table = db.Table("track_playlist_association_table", db.Model.metadata,
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"),primary_key=True),
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True))
from main import db

user_playlist_association_table = db.Table("user_playlist_association_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),primary_key=True),
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True))
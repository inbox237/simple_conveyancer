from main import ma
from models.Playlist import Playlist
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class PlaylistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Playlist
    
    playlist_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many=True)
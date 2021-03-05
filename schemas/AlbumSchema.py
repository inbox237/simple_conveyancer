from main import ma
from models.Album import Album
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
    
    album_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)
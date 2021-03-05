from main import ma
from models.Artist import Artist
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
    
    artist_name = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
from main import ma
from models.Track import Track
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track
    
    track_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)
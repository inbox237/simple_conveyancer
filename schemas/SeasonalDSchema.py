from main import ma
from models.SeasonalD import SeasonalD
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class SeasonalDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SeasonalD
    
    seasonald_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

seasonald_schema = SeasonalDSchema()
seasonalds_schema = SeasonalDSchema(many=True)
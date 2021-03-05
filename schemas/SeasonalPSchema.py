from main import ma
from models.SeasonalP import SeasonalP
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class SeasonalPSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SeasonalP
    
    seasonalp_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

seasonalp_schema = SeasonalPSchema()
seasonalps_schema = SeasonalPSchema(many=True)
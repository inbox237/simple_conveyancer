from main import ma

from models.Settlement import Settlement

from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class SettlementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Settlement
    
    settlement_title = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

settlement_schema = SettlementSchema()
settlements_schema = SettlementSchema(many=True)
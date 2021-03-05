from models.User import User
from models.Settlement import Settlement

from models.User_Settlement_Association import user_settlement_association_table as upat

from schemas.UserSchema import user_schema, users_schema
from schemas.SettlementSchema import settlement_schema, settlements_schema

from main import db
from flask import Blueprint, request, jsonify, abort, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

settlements = Blueprint('settlements', __name__, url_prefix="/settlements")

@settlements.route("/", methods=["GET"])
def settlement_index():
    #Retrieve all settlements
    settlements = Settlement.query.all()
    return render_template("settlements.html", settlements=settlements)


@settlements.route("/", methods=["POST"])
@jwt_required
def settlement_create():
    #Create a new settlement
    settlement_fields = settlement_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_settlement = Settlement()
    new_settlement.settlement_title = settlement_fields["settlement_title"]
    
    user.settlements.append(new_settlement)

    db.session.add(new_settlement)
    db.session.commit()
    
    return jsonify(settlement_schema.dump(new_settlement))

@settlements.route("/<int:id>", methods=["GET"])
@jwt_required
def settlement_show(id):
    #Return a single settlement
    settlement = Settlement.query.get(id)
    return jsonify(settlement_schema.dump(settlement))

@settlements.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def settlement_update(id):
    #Update a settlement
    settlement_fields = settlement_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    settlements = Settlement.query.filter_by(id=id)
    
    if settlements.count() != 1:
        return abort(401, description="Unauthorized to update this book")

    settlements.update(settlement_fields)
    db.session.commit()

    return jsonify(settlement_schema.dump(settlements[0]))

@settlements.route("/<int:id>", methods=["DELETE"])
def settlement_delete(id):
    #Delete a settlement
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    settlement = Settlement.query.filter_by(id=id, user_id=user.id).first()

    if not settlement:
        return abort(400)

    db.session.delete(settlement)
    db.session.commit()

    return jsonify(settlement_schema.dump(settlement))
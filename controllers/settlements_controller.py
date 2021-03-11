from models.User import User
from models.Settlement import Settlement

from schemas.UserSchema import user_schema, users_schema
from schemas.SettlementSchema import settlement_schema, settlements_schema

from main import db
from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user

import sys
import datetime

settlements = Blueprint('settlements', __name__, url_prefix="/settlements")

@settlements.route("/newsettlement", methods=["GET"])
def newsettlement():
    return render_template("newsettlement.html")



@settlements.route("/", methods=["GET"])
def settlement_index():
    #Retrieve all settlements
    settlements = Settlement.query.all()
    return render_template("settlements_index.html", settlements=settlements)


@settlements.route("/", methods=["POST"])
@login_required
def settlement_create():
    
    # Create a new settlement
    name = request.form.get("name")

    settdate = datetime.datetime.date(datetime.datetime.strptime(request.form.get("settdate"),'%Y-%m-%d'))

    address = request.form.get("address")

    saleprice = float(request.form.get("saleprice"))
    deposit = float(request.form.get("deposit"))
    ratesamount = float(request.form.get("ratesamount"))
    ratesstatus = request.form.get("ratesstatus")

    

    #create a new Settlement object, with the data received in the request

    
    new_settlement = Settlement()
    new_settlement.name = name
    new_settlement.settdate = settdate
    
    new_settlement.address = address
    new_settlement.user_id = current_user.id

    new_settlement.saleprice = saleprice
    new_settlement.deposit = deposit
    new_settlement.ratesamount = ratesamount
    new_settlement.ratesstatus = ratesstatus

    #calculations for fields
    balance = float((request.form.get("saleprice")))-float((request.form.get("deposit")))
    
    startrates = datetime.date(2020,7,1)
    endrates = datetime.date(2021,6,30)
    ratesdaystotal = endrates-startrates

    #sd = datetime.date(datetime.datetime.strptime(settdate, '%Y,%m,%d'))
    
    ratesdayspaid = endrates-settdate
    ratesdaysunpaid = settdate-startrates

    rdp = ratesdayspaid.days
    rdu = ratesdaysunpaid.days

    ratespaidfloat = float(ratesdayspaid.days)
    ratesdaystotalfloat = float(ratesdaystotal.days)

    ratesoverpaidrate = (ratespaidfloat / ratesdaystotalfloat)
    ratesoverpaid = (ratesoverpaidrate * ratesamount)

    totalbalance = (balance+ratesoverpaid)

    ratesunderpaidrate = (ratesdaysunpaid.days / ratesdaystotal.days)
    ratesunderpaid = (ratesunderpaidrate * ratesamount)

    totalbalanceunpaid = (balance - ratesunderpaid)
    


    #Calculated fields from above
    new_settlement.ratesoverpaid = saleprice
    new_settlement.ratesunderpaid = ratesunderpaid

    new_settlement.balance = balance

    new_settlement.ratesdayspaid = rdp
    new_settlement.ratesdaysunderpaid = rdu

    new_settlement.totalbalance = saleprice





    #add a new Settlement to the db
    db.session.add(new_settlement)
    db.session.commit()

    #return jsonify(shelter_schema.dump(new_settlement))
    return redirect(url_for('settlements.settlement_index'))




@settlements.route("/<int:id>", methods=["GET"])
#@jwt_required
def settlement_show(id):
    #Return a single settlement
    settlement = Settlement.query.get(id)
    #return jsonify(settlement_schema.dump(settlement))
    return render_template("settlements.html", settlement = settlement )

@settlements.route("/<int:id>", methods=["PUT", "PATCH"])
#@jwt_required
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




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

    new_settlement.saleprice = "{:.2f}".format(saleprice)
    new_settlement.deposit = "{:.2f}".format(deposit)
    new_settlement.ratesamount = "{:.2f}".format(ratesamount)
    new_settlement.ratesstatus = ratesstatus

    #calculations for fields
    balance = float((request.form.get("saleprice")))-float((request.form.get("deposit")))
    
    startrates = datetime.date(2020,7,1)
    endrates = datetime.date(2021,6,30)
    ratesdaystotal = endrates-startrates

    ratesdayspaid = endrates-settdate
    ratesdaysunpaid = settdate-startrates

    rdp = ratesdayspaid.days
    rdu = ratesdaysunpaid.days

    ratespaidfloat = float(ratesdayspaid.days)
    ratesdaystotalfloat = float(ratesdaystotal.days)

    ratesoverpaidrate = (ratespaidfloat / ratesdaystotalfloat)
    ratesunderpaidrate = (ratesdaysunpaid.days / ratesdaystotal.days)
    
    ratesoverpaid = (ratesoverpaidrate * ratesamount)
    ratesunderpaid = (ratesunderpaidrate * ratesamount)

    


    #Calculated fields from above
    if ratesstatus == "on":
        new_settlement.ratesoverpaid = "{:.2f}".format(ratesoverpaid)
        new_settlement.ratesdayspaid = rdp
        new_settlement.ratesunderpaid = "{:.2f}".format(0)
        new_settlement.ratesdaysunpaid = 0
        totalbalance = (balance+ratesoverpaid)

    else:
        new_settlement.ratesunderpaid = "{:.2f}".format(ratesunderpaid)
        new_settlement.ratesdaysunpaid = rdu
        new_settlement.ratesoverpaid = "{:.2f}".format(0)
        new_settlement.ratesdayspaid = 0
        totalbalance = (balance-ratesunderpaid)

    
    new_settlement.balance = "{:.2f}".format(balance)
    new_settlement.totalbalance = "{:.2f}".format(totalbalance)

    #add a new Settlement to the db
    db.session.add(new_settlement)
    db.session.commit()

    #return jsonify(settlement_schema.dump(new_settlement))
    return redirect(url_for('settlements.settlement_index'))




@settlements.route("/<int:id>", methods=["GET"])
#@jwt_required
def settlement_show(id):
    #Return a single settlement
    settlement = Settlement.query.get(id)
    #return jsonify(settlement_schema.dump(settlement))
    return render_template("settlements.html", settlement = settlement )



@settlements.route("/update/<int:id>", methods=["POST"])
@login_required
def settlement_update(id):
    #make sure the selected settlement is owned by the logged in user
    settlement = Settlement.query.filter_by(id=id, user_id=current_user.id).first()
    if not settlement:
        return abort(400, description="Not authorized to delete other people's settlements")

    # Create a new settlement
    print("hello")
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

    new_settlement.saleprice = "{:.2f}".format(saleprice)
    new_settlement.deposit = "{:.2f}".format(deposit)
    new_settlement.ratesamount = "{:.2f}".format(ratesamount)
    new_settlement.ratesstatus = ratesstatus

    #calculations for fields
    balance = float((request.form.get("saleprice")))-float((request.form.get("deposit")))
    
    startrates = datetime.date(2020,7,1)
    endrates = datetime.date(2021,6,30)
    ratesdaystotal = endrates-startrates

    ratesdayspaid = endrates-settdate
    ratesdaysunpaid = settdate-startrates

    rdp = ratesdayspaid.days
    rdu = ratesdaysunpaid.days

    ratespaidfloat = float(ratesdayspaid.days)
    ratesdaystotalfloat = float(ratesdaystotal.days)

    ratesoverpaidrate = (ratespaidfloat / ratesdaystotalfloat)
    ratesunderpaidrate = (ratesdaysunpaid.days / ratesdaystotal.days)
    
    ratesoverpaid = (ratesoverpaidrate * ratesamount)
    ratesunderpaid = (ratesunderpaidrate * ratesamount)

    #Calculated fields from above
    if ratesstatus == "on":
        new_settlement.ratesoverpaid = "{:.2f}".format(ratesoverpaid)
        new_settlement.ratesdayspaid = rdp
        new_settlement.ratesunderpaid = "{:.2f}".format(0)
        new_settlement.ratesdaysunpaid = 0
        totalbalance = (balance+ratesoverpaid)

    else:
        new_settlement.ratesunderpaid = "{:.2f}".format(ratesunderpaid)
        new_settlement.ratesdaysunpaid = rdu
        new_settlement.ratesoverpaid = "{:.2f}".format(0)
        new_settlement.ratesdayspaid = 0
        totalbalance = (balance-ratesunderpaid)

    new_settlement.balance = "{:.2f}".format(balance)
    new_settlement.totalbalance = "{:.2f}".format(totalbalance)

    #save the changes
    db.session.commit()
    #return jsonify(settlement_schema.dump(settlements[0]))
    return redirect(url_for('settlements.settlement_index'))


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


@settlements.route("/modify/<int:id>", methods=["GET"])
def modify_settlement(id):
    settlement = Settlement.query.get(id)
    return render_template("modify_settlement.html", settlement=settlement)

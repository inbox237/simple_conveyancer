from main import db




class Settlement(db.Model):
    __tablename__ = "settlements"
    
    id = db.Column(db.Integer, primary_key=True)
    #settlement_s_tracks_count = db.Column(db.Integer())
    #settlement_s_users_count = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    name = db.Column(db.String())
    settdate = db.Column(db.String())
    address = db.Column(db.String())
    saleprice = db.Column(db.String())
    deposit = db.Column(db.String())
    ratesamount = db.Column(db.String())
    ratesstatus = db.Column(db.String())
    
    balance = db.Column(db.String())
    ratesdayspaid = db.Column(db.Integer())
    ratesdaysunpaid = db.Column(db.Integer())
    ratesoverpaid = db.Column(db.String())
    ratesunderpaid = db.Column(db.String())

    totalbalance = db.Column(db.String())

    
    # def __repr__(self):
    #     return f"<Track {self.settlement_title}>"

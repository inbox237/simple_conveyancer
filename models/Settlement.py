from main import db




class Settlement(db.Model):
    __tablename__ = "settlements"
    
    id = db.Column(db.Integer, primary_key=True)
    settlement_title = db.Column(db.String())
    settlement_s_tracks_count = db.Column(db.Integer())
    settlement_s_users_count = db.Column(db.Integer())
    settlement_s_users = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    
    def __repr__(self):
        return f"<Track {self.settlement_title}>"

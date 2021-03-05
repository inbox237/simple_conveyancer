from main import db

from models.User_Settlement_Association import user_settlement_association_table as upat


class Settlement(db.Model):
    __tablename__ = "settlements"
    
    id = db.Column(db.Integer, primary_key=True)
    settlement_title = db.Column(db.String())
    settlement_s_tracks_count = db.Column(db.Integer())
    settlement_s_users_count = db.Column(db.Integer())
    settlement_s_users = db.relationship("User",
                        secondary=upat,
                        back_populates="user_s_settlements")

    def __repr__(self):
        return f"<Track {self.settlement_title}>"

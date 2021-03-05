from main import db

from models.User_Settlement_Association import user_settlement_association_table as upat

from models.Settlement import Settlement

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    user_s_settlements_count = db.Column(db.Integer())
    user_s_settlements = db.relationship("Settlement", secondary=upat,
                        back_populates="settlement_s_users")


    def __repr__(self):
        return f"<User {self.email}>"
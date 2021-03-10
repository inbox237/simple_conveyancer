from main import db
from models.Settlement import Settlement
from flask_login import UserMixin

def get_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    return user

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=True, unique=True)
    username = db.Column(db.String(), nullable=True, unique=True)
    password = db.Column(db.String(), nullable=False)
    user_s_settlements_count = db.Column(db.Integer())
    user_s_settlements = db.relationship("Settlement", backref="user")

    def __repr__(self):
        return f"<User {self.email}>"
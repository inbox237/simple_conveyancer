from main import db


class SeasonalD(db.Model):
    __tablename__ = "seasonalds"
    
    id = db.Column(db.Integer, primary_key=True)
    user_ids = db.relationship("User", backref="seasonalds", lazy=True)
    seasonald_title = db.Column(db.String())
    seasonald_offer = db.Column(db.Float())
    
    def __repr__(self):
        return f"<Artist {self.seasonald_title}>"
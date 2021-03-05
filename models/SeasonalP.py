from main import db


class SeasonalP(db.Model):
    __tablename__ = "seasonalps"
    
    id = db.Column(db.Integer, primary_key=True)
    user_ids = db.relationship("User", backref="seasonalps", lazy=True)
    seasonalp_title = db.Column(db.String())
    seasonalp_desc = db.Column(db.String())
    
    def __repr__(self):
        return f"<Artist {self.seasonalp_title}>"
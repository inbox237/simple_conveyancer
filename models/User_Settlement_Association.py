from main import db

user_settlement_association_table = db.Table("user_settlement_association_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),primary_key=True),
    db.Column("settlement_id", db.Integer, db.ForeignKey("settlements.id"), primary_key=True))
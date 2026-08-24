import sqlalchemy as db
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from datetime import datetime
from .users import User


class Seller(SqlAlchemyBase):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.VARCHAR, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    user = orm.relationship('User')

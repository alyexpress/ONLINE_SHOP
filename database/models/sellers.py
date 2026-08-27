from ..session import SqlAlchemyBase
import sqlalchemy as db

from datetime import datetime
from sqlalchemy import orm
from . import User


class Seller(SqlAlchemyBase):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    shop_name = db.Column(db.VARCHAR, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0)
    created_date = db.Column(db.DateTime, default=datetime.now())

    # ORM models connection
    user = orm.relationship('User')

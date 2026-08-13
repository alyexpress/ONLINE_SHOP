import sqlalchemy as db
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from datetime import datetime
from .sellers import Seller

class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    seller = orm.relationship('Seller')

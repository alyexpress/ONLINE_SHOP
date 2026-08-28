from ..session import SqlAlchemyBase
import sqlalchemy as db

from datetime import datetime
from sqlalchemy import orm


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    img_src = db.Column(db.String, nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    checked = db.Column(db.Boolean, nullable=True, default=False)
    discount_price = db.Column(db.Float, nullable=True)
    count = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

    # ORM models connection
    seller = orm.relationship('Seller')
    category = orm.relationship('Category')

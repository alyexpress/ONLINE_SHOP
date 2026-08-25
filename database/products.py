import sqlalchemy as db
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from datetime import datetime
from .sellers import Seller
from .categories import Category

class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    count = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    seller = orm.relationship('Seller')
    category = orm.relationship('Category')

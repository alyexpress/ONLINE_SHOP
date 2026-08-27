from ..session import SqlAlchemyBase
import sqlalchemy as db

from datetime import datetime
from sqlalchemy import orm
from . import Product


class Transaction(SqlAlchemyBase):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)

    # === TRANSACTION TYPES ===
    # 0    (website -> user)
    # 1    (user -> seller)
    # 2    (seller -> website)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    from_id = db.Column(db.Integer, nullable=True)
    to_id = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

    # ORM models connection
    product = orm.relationship('Product')

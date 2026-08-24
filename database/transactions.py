import sqlalchemy as db
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from datetime import datetime
from .products import Product

class Transaction(SqlAlchemyBase):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    transaction_type = db.Column(db.Integer, nullable=False)
    from_id = db.Column(db.Integer, nullable=True)
    to_id = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    product = orm.relationship('Product')

    # === TRANSACTION TYPES ===
    # 0    (user -> website)
    # 1    (user -> seller)
    # 2    (website -> user)

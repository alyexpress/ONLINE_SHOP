from ..session import SqlAlchemyBase
import sqlalchemy as db

from datetime import datetime
from sqlalchemy import orm

class Rating(SqlAlchemyBase):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    rating = db.Column(db.Integer, nullable=False, default=0)

    # ORM models connection
    product = orm.relationship('Product')
    user = orm.relationship('Users')
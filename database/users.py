import sqlalchemy as db
from .db_session import SqlAlchemyBase
from datetime import datetime


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR, unique=True, nullable=False)
    username = db.Column(db.VARCHAR, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

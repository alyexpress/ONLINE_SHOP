import sqlalchemy as db
from .db_session import SqlAlchemyBase
from datetime import datetime
from flask_login import UserMixin
from app.utils import hashed_password


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR, unique=True, nullable=False)
    username = db.Column(db.VARCHAR, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    created_date = db.Column(db.DateTime, default=datetime.now())

    def check_password(self, password):
        return self.hashed_password == hashed_password(password)

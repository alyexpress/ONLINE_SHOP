import sqlalchemy as db
from .db_session import SqlAlchemyBase

class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR, nullable=False)
    img_url = db.Column(db.String, nullable=False)
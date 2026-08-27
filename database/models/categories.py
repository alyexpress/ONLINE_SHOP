from ..session import SqlAlchemyBase
import sqlalchemy as db

class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR, unique=True, nullable=False)
    img_src = db.Column(db.String, nullable=False)
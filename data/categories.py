import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    building = orm.relation("Building", back_populates='categories')
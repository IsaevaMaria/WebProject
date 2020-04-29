import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Building(SqlAlchemyBase):
    __tablename__ = 'building'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String)
    adress = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("categories.id"))
    categories = orm.relation('Categories')
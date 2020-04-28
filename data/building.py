import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Building(SqlAlchemyBase):
    __tablename__ = 'building'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("categoria.id"))
    categor = orm.relation('Categoria')
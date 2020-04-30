import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Routes(SqlAlchemyBase):
    __tablename__ = 'routes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    building = orm.relation("Building", back_populates='routes')
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    

    def __repr__(self):
        return self.name

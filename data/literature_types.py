import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class LiteratureTypes(SqlAlchemyBase):
    __tablename__ = 'literature_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    

    def __repr__(self):
        return self.name

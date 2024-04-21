import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String)
    type_of_fiction_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("literature_types.id"))
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
    publish_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    path_to_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    genre = orm.relationship("Genres")
    type_of_fiction = orm.relationship("LiteratureTypes")

    def __repr__(self):
        return f'<Book> {self.title}, {self.author}'

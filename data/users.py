import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    rights = sqlalchemy.Column(sqlalchemy.String)


    def __repr__(self):
        if self.rights == "user":
            return f'<User> {self.id} {self.surname} {self.name}'
        elif self.rights == "administrator":
            return f"<Administator> {self.id} {self.surname} {self.name}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

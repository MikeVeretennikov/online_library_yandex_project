from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, FieldList
from wtforms.validators import DataRequired


class AddBook(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    type_of_fiction_id = IntegerField("ID рода литературы", validators=[DataRequired()])
    genre_id = IntegerField("ID жанра литературы", validators=[DataRequired()])
    publish_year = IntegerField("Год публикации")
    path_to_file = StringField("Путь к файлу в формате 'book_files/path.txt'")
        
    submit = SubmitField('Подтвердить')

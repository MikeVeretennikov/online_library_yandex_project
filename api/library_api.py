import flask
import flask_login

from data import db_session
from data.books import Book


blueprint = flask.Blueprint(
    "library_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/books")
def get_books():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    
    if not books:
        flask.abort(404)

    
    return flask.jsonify(
        {
            'books': [item.to_dict() for item in books]
        })
    
    
    

@blueprint.route('/api/books', methods=['POST'])
def add_book():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['title', 'author', 'type_of_fiction_id', 'genre_id', "publish_year", "path_to_file"]):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    book = Book(
        title=flask.request.json['title'],
        author=flask.request.json['author'],
        type_of_fiction_id=flask.request.json['type_of_fiction_id'],
        genre_id=flask.request.json['genre_id'],
        publish_year=flask.request.json['publish_year'],
        path_to_file = flask.request.json["path_to_file"]
    )
    db_sess.add(book)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route("/api/genre_books/<int:genre_id>")
def get_genre_books(genre_id):
    db_sess = db_session.create_session()
    books = db_sess.query(Book).filter(Book.genre_id == genre_id)
    
    if not books:
        flask.abort(404)
    
    return flask.jsonify(
        {
            'books': [item.to_dict() for item in books]
        })
    
    
@blueprint.route("/api/author_books/<string:author_name>")
def get_author_books(author_name):
    db_sess = db_session.create_session()
    books = db_sess.query(Book).filter(Book.author == author_name)
    
    if not books:
        flask.abort(404)
    
    return flask.jsonify(
        {
            'books': [item.to_dict() for item in books]
        })
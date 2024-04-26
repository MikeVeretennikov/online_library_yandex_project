import flask
import flask_login


from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.add_book_form import AddBook
from data import db_session
from data.users import User
from data.books import Book
from data.genres import Genres
from api import library_api


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "library"



login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
    

@app.route("/")
def index():
    
    sess = db_session.create_session()
    
    books = sess.query(Book).all()
    
    
    return flask.render_template("index.html", books=books, title="Онлайн библиотека")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): # POST обработка
        
        if form.password.data != form.password_again.data: # Если пароли не совпадают
            return flask.render_template('register.html', title='Регистрация', form=form,
                                         message="Пароли не совпадают")
        
        db_sess = db_session.create_session()
        
        if db_sess.query(User).filter(User.email == form.email.data).first(): # Если пользователь с таким же email уже есть
            return flask.render_template('register.html', title='Регистрация', form=form,
                                         message="Такой пользователь уже существует")
            
        # Создаем нового пользователя
        
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.rights = "user"
        user.set_password(form.password.data)
        
        db_sess.add(user)
        db_sess.commit()
        
        return flask.redirect("/login")
        
    # GET обработка
    return flask.render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        
        if user and user.check_password(form.password.data):
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
    
    return flask.render_template("login.html", title="Вход", form=form)


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/download/<int:book_id>")
def download_book(book_id):
    sess = db_session.create_session()
    book = sess.query(Book).filter(Book.id == book_id).first()

    return flask.send_file(book.path_to_file, as_attachment=True)


@app.route("/add_book", methods=["GET", "POST"])
@flask_login.login_required
def add_book():
    form = AddBook()

    if flask.request.method == "POST":
        sess = db_session.create_session()
        book = Book(
            title = form.title.data,
            author = form.author.data, 
            type_of_fiction_id = form.type_of_fiction_id.data,
            genre_id = form.genre_id.data,
            publish_year = form.publish_year.data,
            path_to_file = form.path_to_file.data
        )
        
        sess.add(book)
        sess.commit()
        return flask.redirect("/")

    elif flask.request.method == "GET":
        return flask.render_template("add_book.html", title="Добавление книги", form=form)


@app.route("/delete_book/<int:book_id>")
@flask_login.login_required
def delete_book(book_id):
    sess = db_session.create_session()
    book = sess.query(Book).filter(Book.id == book_id).first()
    
    if book:
        sess.delete(book)
        sess.commit()
    else:
        flask.abort(404)
    
    return flask.redirect("/")


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
@flask_login.login_required
def edit_book(book_id):
    form = AddBook()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        book = db_sess.query(Book).filter(Book.id == book_id).first()
        
        if book:
            form.title.data = book.title
            form.author.data = book.author
            form.type_of_fiction_id.data = book.type_of_fiction_id
            form.genre_id.data = book.genre_id
            form.publish_year.data = book.publish_year
            form.path_to_file.data = book.path_to_file
        else:
            flask.abort(404)
    
    elif flask.request.method == "POST":
        db_sess = db_session.create_session()
        book = db_sess.query(Book).filter(Book.id == book_id).first()
        
        if book:
            book.title = form.title.data
            book.author = form.author.data
            book.type_of_fiction_id = form.type_of_fiction_id.data
            book.genre_id = form.genre_id.data
            book.publish_year = form.publish_year.data
            book.path_to_file = form.path_to_file.data
            db_sess.commit()
            
            return flask.redirect("/")
        else:
            flask.abort(404)
    
    return flask.render_template("add_book.html", title="Редактирование книги", form=form)


def main():
    db_session.global_init("db/online_library.db")
    
    app.register_blueprint(library_api.blueprint)
    app.run()


if __name__ == "__main__":
    main()
import flask
import flask_login

from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from data import db_session
from data.users import User
from data.books import Book
from data.genres import Genre


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


def main():
    db_session.global_init("db/online_library.db")
    

    app.run()


if __name__ == "__main__":
    main()
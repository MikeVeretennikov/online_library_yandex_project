from data import db_session
from data.users import User


db_session.global_init("db/online_library.db")

sess = db_session.create_session()


def ask_id():
    id = input("Введите id пользователя, которому хотите назначить права администратора:\n")
    while not id.isdigit():
        id = input("Введите id пользователя, которому хотите назначить права администратора:\n")
    return int(id)


user_id = ask_id()
future_admin = sess.query(User).filter(User.id == user_id).first()

while not future_admin: 
    print("Пользователя с таким id нет")
    print("Введите id заново\n")
    user_id = ask_id()
    future_admin = sess.query(User).filter(User.id == user_id).first()
    
future_admin.rights = "administrator"
sess.commit()
print(f"Вы успешно назначили права администратора пользователю {future_admin} права администратора")
    

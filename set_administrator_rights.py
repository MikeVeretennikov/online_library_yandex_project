from data import db_session
from data.users import User


db_session.global_init("db/online_library.db")

sess = db_session.create_session()


def ask_id():
    id = input("Enter the id of the user to whom you want to assign administrator rights:\n")
    while not id.isdigit():
        id = input("Enter the id of the user to whom you want to assign administrator rights:\n")
    return int(id)


user_id = ask_id()
future_admin = sess.query(User).filter(User.id == user_id).first()

while not future_admin: 
    print("There is no user with this id")
    print("Re-enter id\n")
    user_id = ask_id()
    future_admin = sess.query(User).filter(User.id == user_id).first()
    
future_admin.rights = "administrator"
sess.commit()
print(f"You have successfully assigned administrator rights to a user {future_admin} administrator rights")
    

import sqlite3

admin = False
user_id = 0


def check_admin(u_password, u_name):
    global user_id
    con = sqlite3.connect('AppClock_users_db.db')
    cur = con.cursor()
    result_password = cur.execute(f"""SELECT id 
                FROM Passwords WHERE Password = {u_password}""").fetchall()
    result_name = cur.execute(f"""SELECT id FROM User 
        WHERE Name = '{u_name}'""").fetchall()
    id_user = cur.execute(f"""SELECT id FROM All_inf_user
                WHERE PasswordId = '{result_password[0][0]}' and NameId = '{result_name[0][0]}'""").fetchall()
    con.close()
    user_id = id_user[0][0]
    if id_user[0][0] == 1:
        return True
    return False


def save(examination):
    global admin
    if examination:
        admin = True

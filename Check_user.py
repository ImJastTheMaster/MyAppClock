import sqlite3


def check(u_password, u_name):
    con = sqlite3.connect('AppClock_users_db.db')
    cur = con.cursor()
    result_password = cur.execute(f"""SELECT id 
            FROM Passwords WHERE Password = {u_password}""").fetchall()
    result_name = cur.execute(f"""SELECT id FROM User 
    WHERE Name = '{u_name}'""").fetchall()
    if result_name == [] or result_password == []:
        return False
    id = cur.execute(f"""SELECT id FROM All_inf_user
            WHERE PasswordId = '{result_password[0][0]}' and NameId = '{result_name[0][0]}'""").fetchall()
    con.close()
    if id != []:
        return True
    return False


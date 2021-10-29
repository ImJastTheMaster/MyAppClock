import sqlite3


def check(u_password, u_name):
    con = sqlite3.connect('AppClock_users_db.db')
    cur = con.cursor()
    result_password = cur.execute(f"""SELECT id 
            FROM Passwords WHERE Password = {u_password}""").fetchall()
    result_name = cur.execute(f"""SELECT id FROM User 
    WHERE Name = '{u_name}'""").fetchall()
    con.close()
    if result_name == [] or result_password == []:
        return False
    if result_name[0][0] == result_password[0][0]:
        return True
    return False


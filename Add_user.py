import sqlite3, Check_user


def get_result(u_password, u_name, u_surname, u_patronymic):
    try:
        con = sqlite3.connect('AppClock_users_db.db')
        cur = con.cursor()
        if Check_user.check(u_password, u_name) is False:
            cur.execute(f"""INSERT INTO User(Name, Surname, Patronymic)
            VALUES('{u_name}', '{u_surname}', '{u_patronymic}')""")
            cur.execute(f"""INSERT INTO Passwords(Password)
            VALUES('{u_password}')""")
            con.commit()
            result_password = cur.execute(f"""SELECT id FROM Passwords WHERE Password = '{u_password}'""").fetchall()
            result_name = cur.execute(f"""SELECT id FROM User WHERE Name = '{u_name}'""").fetchall()
            cur.execute(f"""INSERT INTO All_inf_user(PasswordId, NameId)
            VALUES('{result_password[0][0]}', '{result_name[0][0]}')""")
            con.commit()
            return True
        return False
    except sqlite3.IntegrityError:
        return False
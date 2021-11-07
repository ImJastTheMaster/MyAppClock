import ctypes, sqlite3, function_save

QSS = """
#my_timer {
    border-image: url(./Arts/Egypt.jpg) 0 0 0 0 stretch stretch;
}
#my_time {
    border-image: url(./Arts/art-london.jpg) 0 0 0 0 stretch stretch;
}
#reg_widget {
    border-image: url(./Arts/new_york.jpg) 0 0 0 0 stretch stretch;
}
#widget {
    border-image: url(./Arts/moon-sky.jpg) 0 0 0 0 stretch stretch;
}
#my_stopwatch {
    border-image: url(./Arts/Paris.jpg) 0 0 0 0 stretch stretch;
}
#my_alarm {
    border-image: url(./Arts/kitaiskaya-stena.jpg) 0 0 0 0 stretch stretch;
}
#play_widget {
    border-image: url(./Arts/rabstol_net_fields_12_2560x1440.jpg) 0 0 0 0 stretch stretch;
}
"""
user32 = ctypes.windll.user32
SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SECONDS = 60
FULL_PROGRESS = 100
MAX_LEN = 1000
TIME_SET = 1000
MIN_LEN = 100
MINI_LEN = 10
DAY_ON_MOUNTH = 30
NOT_INDEX = 999999999999999999
LOW_STR_LEN = 0
MAX_STR_LEN = 2
DISTANCE_ONE = 17
DISTANCE_TWO = 14
FNAME = 'mellen_gi_remix_na_budilnik.mp3'


def len_object(name):
    if len(str(name)) == 2:
        return '' + str(name)
    elif len(str(name)) == 1:
        return '0' + str(name)


def sorted_alarms():
    all_alarms_sorted = []
    all_alarms_not_sorted = []
    return_list = []
    con = sqlite3.connect('AppClock_users_db.db')
    cur = con.cursor()
    for i in cur.execute(f"""SELECT alarm 
            FROM Dates WHERE UserId = '{function_save.user_id}'""").fetchall():
        all_alarms_sorted.append(str(i[0]))
        all_alarms_not_sorted.append(
            [str(i[0]).split()[-1], str(i[0]).split()[0].split('-'),
             str(i[0]).split()[1].split(':')])
    all_alarms_not_sorted = sorted(all_alarms_not_sorted,
                                   key=lambda x: (int(x[1][0]), int(x[1][1]), int(x[1][2]),
                                                  int(x[2][0]), int(x[2][1]), int(x[2][2])))
    for i in all_alarms_not_sorted:
        for j in all_alarms_sorted:
            alarm_str = '-'.join(list(map(str, i[1]))) + ' ' + \
                        ':'.join(list(map(str, i[2]))) + ' - ' + i[0]
            if str(alarm_str) == str(j):
                return_list.append(j)
    return return_list

import sys, constants, calendar, sqlite3, function_save, datetime
from constants import SECONDS, FULL_PROGRESS, MIN_LEN, MAX_LEN, TIME_SET, MINI_LEN

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer


class Time(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Time.ui', self)
        self.setWindowTitle('AppClock')
        self.setGeometry((constants.SCREENSIZE[0] - 415) // 2, (constants.SCREENSIZE[1] - 557) // 2, 415, 557)
        self.flag = False
        self.sec = 0
        self.min = 0
        self.msec = 0
        self.last = 0
        self.flag_two = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(TIME_SET)
        self.show_time()
        self.start.clicked.connect(self.countdown)
        self.reset.clicked.connect(self.restart)
        self.stop.clicked.connect(self.stopping)
        self.start_stopwatch.clicked.connect(self.starting)
        self.interval.clicked.connect(self.add_interval)
        self.stop_stopwatch.clicked.connect(self.stop_watch)
        self.clear_list.clicked.connect(self.clear)
        self.total = 1
        self.list_times.addItem(f'Сircle            Total time             Lap time')
        self.list_times.addItem(f'--------------------------------------------------')
        self.minute_num = 0
        self.seconds_num = 0
        self.msseconds_num = 0
        con = sqlite3.connect('AppClock_users_db.db')
        cur = con.cursor()
        self.all_alarms.clear()
        for i in cur.execute(f"""SELECT alarm 
                        FROM Dates WHERE UserId = '{function_save.user_id}'""").fetchall():
            self.all_alarms.addItem(str(i[0]))
        self.add_alarm.clicked.connect(self.go_add_alarm)
        con.close()

    def go_add_alarm(self):
        # переходим в календарь для добавления будтльника
        self.cal = calendar.MyCalendar()
        self.cal.show()
        Time().hide()
        self.hide()

    def stop_watch(self):
        # останавливаем секундомер
        if self.flag_two is False:
            return 0
        self.flag_two = False
        self.start_stopwatch.setText('Proceed')

    def clear(self):
        # очищаем секундомер
        self.total = 1
        self.last = 0
        self.list_times.clear()
        self.list_times.addItem(f'Сircle            Total time             Lap time')
        self.list_times.addItem(f'--------------------------------------------------')
        self.stopwatch_l.setText(f'{"00"}:{"00"}.{"00"}')
        self.flag_two = False
        self.start_stopwatch.setText('Start')

    def add_interval(self):
        # добавляем интервал
        if self.flag_two is False:
            return 0
        now_time = int(self.stopwatch_l.text().split(":")[0]) * MIN_LEN + \
                   int(self.stopwatch_l.text().split(":")[1].split(".")[0])
        dif = now_time - self.last
        if now_time - self.last < MAX_LEN:
            difference = '0'
        else:
            difference = ''
        if now_time - self.last < MINI_LEN:
            difference_sec = '0'
        else:
            difference_sec = ''
        null = ''
        diff = 0
        if self.total >= 10:
            diff = 2
        if int(self.stopwatch_l.text().split(":")[1].split(".")[1]) < 10:
            null = '0'
        time_watch = (difference + str(dif // MIN_LEN)) + ":" + difference_sec + str(dif) + \
                     "." + null + self.stopwatch_l.text().split(":")[1].split(".")[1]
        all_watch = self.stopwatch_l.text()[0:5] + \
                    "." + null + self.stopwatch_l.text().split(":")[1].split(".")[1]
        self.list_times.addItem(f'{self.total}{" " * (17 - diff)}{all_watch}{" " * 14}'
                                f'{time_watch}')
        self.total += 1
        self.last = now_time

    def starting(self):
        # запускаем секундомер
        if self.flag_two is False:
            self.flag_two = True
            self.tick_timer()

    def restart(self):
        # сброс всех значений таймера
        self.flag = False
        self.start.setText('Start')
        self.seconds.setValue(0)
        self.minutes.setValue(0)
        self.hours.setValue(0)
        self.seconds.setEnabled(True)
        self.minutes.setEnabled(True)
        self.hours.setEnabled(True)
        self.progressTime.setValue(0)

    def stopping(self):
        # остановка таймера
        if self.seconds.value() == 0 and self.minutes.value() == 0 \
                and self.hours.value() == 0:
            return False
        if self.start.text() != 'Proceed':
            self.flag = False
            self.start.setText('Proceed')

    def countdown(self):
        # продожение таймера
        self.flag = True
        if self.start.text() != 'Proceed':
            self.progressTime.setValue(0)
            self.set_seconds = self.seconds.value()
            self.set_minutes = self.minutes.value()
            self.set_hours = self.hours.value()
            self.all_time = int(self.seconds.value()) + \
                            int(self.minutes.value()) * SECONDS + \
                            int(self.hours.value()) * SECONDS * SECONDS
            if self.all_time == 0:
                self.flag = False

    def tick_timer(self):
        # высчитываем значение секундомера
        if self.flag_two:
            self.msseconds_num += 1
            self.seconds_num = (self.msseconds_num // 100) % 60
            self.minute_num = self.msseconds_num // 100 // 60
            if self.minute_num < 10:
                num_mint = 1
            else:
                num_mint = 0
            if self.seconds_num < 10:
                num_sec = 1
            else:
                num_sec = 0
            if self.msseconds_num < 10:
                num_ms = 1
            else:
                num_ms = 0
            self.stopwatch_l.setText(f'{"0" * num_mint + str(self.minute_num)}:{"0" * num_sec + str(self.seconds_num)}.'
                                     f'{"0" * num_ms + str(self.msseconds_num % 100)}')
            QTimer().singleShot(10, self.tick_timer)

    def show_time(self):
        # выполняем посчёты для мирового, таймера и также находим время до ближайшего будильника
        now_time = QTime.currentTime()
        text = now_time.toString('hh:mm:ss')
        self.time.setText(text)
        self.time_m.setText(text[0:5])
        self.time_l.setText(str(int(text[0:2]) - 2) + ':' + text[3:5])
        self.time_ny.setText(str(int(text[0:2]) - 7) + ':' + text[3:5])
        if self.all_alarms.count() != 0:
            now_datetime = datetime.datetime.now()
            alarm = self.all_alarms.item(0).text()
            diff_year = int(alarm[0:4]) - int(str(now_datetime)[0:4])
            days = int(alarm[5:7]) - int(str(now_datetime)[5:7]) * constants.DAY_ON_MOUNTH - \
                       int(alarm[8:10]) - int(str(now_datetime)[8:10])
            diff_day = datetime.timedelta(days=days)
            diff_mouth = (now_datetime + diff_day).month
            if (now_datetime + diff_day).month >= 12:
                diff_mouth %= 12
                diff_year += diff_mouth // 12
            alarms = [alarm[11:13], alarm[14:16], alarm[17:19]]
            hour_min_sec = [alarm[11:13], alarm[14:16], alarm[17:19]]
            for i in alarms:
                if i == '00':
                    hour_min_sec[alarms.index(i)] = 0
            diff_hour = int(hour_min_sec[0]) - int(str(now_datetime)[11:13])
            diff_minutes = int(hour_min_sec[1]) - int(str(now_datetime)[14:16])
            diff_seconds = int(hour_min_sec[2]) - int(str(now_datetime)[17:19])
            self.closest_alarm.setText(str('{}-{}-{} {}:{}:{}'.format(diff_year, diff_mouth,
                                             (now_datetime + diff_day).day,
                                             diff_hour, diff_minutes, diff_seconds)))
        if self.flag:
            self.now_all_time = int(self.seconds.value()) + \
                                int(self.minutes.value()) * SECONDS + \
                                int(self.hours.value()) * SECONDS * SECONDS
            if self.now_all_time == 0:
                self.progressTime.setValue(FULL_PROGRESS)
            else:
                self.progressTime.setValue(FULL_PROGRESS - int(self.now_all_time /
                                                               self.all_time * FULL_PROGRESS))
            self.seconds.setEnabled(False)
            self.minutes.setEnabled(False)
            self.hours.setEnabled(False)
            if self.seconds.value() != 0:
                self.seconds.setValue(int(self.seconds.value()) - 1)
            elif self.seconds.value() == 0 and self.minutes.value() != 0:
                self.seconds.setValue(SECONDS - 1)
                self.minutes.setValue(int(self.minutes.value()) - 1)
            elif self.minutes.value() == 0 and self.hours.value() != 0:
                self.seconds.setValue(SECONDS - 1)
                self.minutes.setValue(SECONDS - 1)
                self.hours.setValue(int(self.hours.value()) - 1)
            elif self.seconds.value() == 0 and self.minutes.value() == 0 \
                    and self.hours.value() == 0:
                self.flag = False
                self.seconds.setValue(self.set_seconds)
                self.minutes.setValue(self.set_minutes)
                self.hours.setValue(self.set_hours)
                self.seconds.setEnabled(True)
                self.minutes.setEnabled(True)
                self.hours.setEnabled(True)
                self.start.setText('Start')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(constants.QSS)
    form = Time()
    form.setFixedSize(415, 557)
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

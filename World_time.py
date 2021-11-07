import sys, sqlite3, datetime
import Planner_mini, constants, function_save, Player_music
from constants import SECONDS, FULL_PROGRESS, MIN_LEN, TIME_SET, \
    MINI_LEN, LOW_STR_LEN, MAX_STR_LEN, DISTANCE_ONE, DISTANCE_TWO
from my_PushButton import AnimationShadowEffect

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QTime, QTimer


class Time(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Design/Time.ui', self)
        self.setWindowTitle('AppClock')
        self.setGeometry((constants.SCREENSIZE[0] - 415) // 2, (constants.SCREENSIZE[1] - 557) // 2, 415, 557)
        self.exit_button.setCheckable(True)
        self.aniButton = AnimationShadowEffect(QtCore.Qt.white, self.exit_button)
        self.exit_button.hover.connect(self.button_hover)
        self.exit_button.setGraphicsEffect(self.aniButton)
        self.flag = False
        self.sec = 0
        self.min = 0
        self.msec = 0
        self.last = 0
        self.flag_two = False
        self.flag_player = False
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
        self.sort_alarm()
        self.add_alarm.clicked.connect(self.go_add_alarm)
        self.delet_alarm.clicked.connect(self.delete_this_alarm)
        self.music_settings.clicked.connect(self.open_music)
        self.music_settings_alarm.clicked.connect(self.open_music)
        self.music_settings_alarm.setToolTip("Settings of music")
        self.music_settings.setToolTip("Settings of music")
        self.exit_button.clicked.connect(self.close)

    def button_hover(self, hover):
        if hover == "enterEvent":
            self.aniButton.start()
        elif hover == "leaveEvent":
            self.aniButton.stop()

    def sort_alarm(self):
        con = sqlite3.connect('AppClock_users_db.db')
        cur = con.cursor()
        self.all_alarms.clear()
        for i in constants.sorted_alarms():
            self.all_alarms.addItem(i)
        con.close()

    def open_music(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                 '', 'Картинка (*.mp3)')[0]
        if self.fname != '':
            constants.FNAME = self.fname

    def delete_this_alarm(self):
        try:
            self.alarm_error.setText('')
            con = sqlite3.connect('AppClock_users_db.db')
            cur = con.cursor()
            cur.execute(f"""DELETE FROM Dates
            WHERE alarm = '{self.all_alarms.selectedItems()[0].text()}' and UserId = '{function_save.user_id}'""")
            con.commit()
            self.all_alarms.clear()
            for i in cur.execute(f"""SELECT alarm 
                            FROM Dates WHERE UserId = '{function_save.user_id}'""").fetchall():
                self.all_alarms.addItem(str(i[0]))
            con.close()
            if self.all_alarms.item(0) is None:
                self.closest_alarm.setText('No alarns')
            self.sort_alarm()
        except IndexError:
            self.alarm_error.setText('No alarm selected')

    def go_add_alarm(self):
        self.cal = Planner_mini.MyCalendar()
        self.cal.setFixedSize(805, 600)
        self.cal.show()
        Time().hide()
        self.hide()

    def stop_watch(self):
        if self.flag_two is False:
            return 0
        self.flag_two = False
        self.start_stopwatch.setText('Proceed')

    def clear(self):
        self.total = 1
        self.last = 0
        self.list_times.clear()
        self.list_times.addItem(f'Сircle            Total time             Lap time')
        self.list_times.addItem(f'--------------------------------------------------')
        self.stopwatch_l.setText(f'{"00"}:{"00"}.{"00"}')
        self.minute_num = 0
        self.seconds_num = 0
        self.msseconds_num = 0
        self.flag_two = False
        self.start_stopwatch.setText('Start')

    def add_interval(self):
        if self.flag_two is False:
            return 0
        now_time = int(self.stopwatch_l.text().split(":")[0]) * MIN_LEN + \
                   int(self.stopwatch_l.text().split(":")[1].split(".")[0])
        dif = now_time - self.last
        diff = LOW_STR_LEN
        if self.total >= MINI_LEN:
            diff = MAX_STR_LEN
        time_watch = (constants.len_object(dif // MIN_LEN)) + ":" + constants.len_object(dif) + \
                     "." + constants.len_object(self.stopwatch_l.text().split(":")[1].split(".")[1])
        all_watch = self.stopwatch_l.text()[0:5] + \
                    "." + constants.len_object(self.stopwatch_l.text().split(":")[1].split(".")[1])
        self.list_times.addItem(f'{self.total}{" " * (DISTANCE_ONE - diff)}{all_watch}{" " * DISTANCE_TWO}'
                                f'{time_watch}')
        self.total += 1
        self.last = now_time

    def starting(self):
        if self.flag_two is False:
            self.flag_two = True
            self.tick_timer()

    def restart(self):
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
        if self.seconds.value() == 0 and self.minutes.value() == 0 \
                and self.hours.value() == 0:
            return False
        if self.start.text() != 'Proceed':
            self.flag = False
            self.start.setText('Proceed')

    def countdown(self):
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
        if self.flag_two:
            self.msseconds_num += 1
            self.seconds_num = (self.msseconds_num // 100) % 60
            self.minute_num = self.msseconds_num // 100 // 60
            self.stopwatch_l.setText(f'{constants.len_object(self.minute_num)}:'
                                     f'{constants.len_object(self.seconds_num)}.'
                                     f'{constants.len_object(self.msseconds_num % 100)}')
            QTimer().singleShot(10, self.tick_timer)

    def show_time(self):
        now_time = QTime.currentTime()
        text = now_time.toString('hh:mm:ss')
        self.time.setText(text)
        self.time_m.setText(text[0:5])
        self.time_l.setText(str(int(text[0:2]) - 2) + ':' + text[3:5])
        self.time_ny.setText(str(int(text[0:2]) - 7) + ':' + text[3:5])
        if self.all_alarms.count() != 0:
            now_datetime = datetime.datetime.now()
            alarm = self.all_alarms.item(0).text()
            alarm_year, alarm_mouth, alarm_day, alarm_hour, alarm_minute, alarm_seconds = \
                int(alarm[0:4]), int(alarm[5:7]), \
                int(alarm[8:10]), int(alarm[11:13]), \
                int(alarm[14:16]), int(alarm[17:19])
            alarm_time = datetime.datetime(alarm_year, alarm_mouth, alarm_day,
                                           alarm_hour, alarm_minute, alarm_seconds)
            difference = (alarm_time - now_datetime).total_seconds()
            days = divmod(difference, 86400)
            hours = divmod(days[1], 3600)
            minutes = divmod(hours[1], 60)
            seconds = divmod(minutes[1], 1)
            self.closest_alarm.setText("%d day  %dh : %dm : %ds" %
                                       (days[0], hours[0], minutes[0], seconds[0]))
            if days[0] == 0 and hours[0] == 0 and minutes[0] == 0 and seconds[0] == 0:
                self.all_alarms.setCurrentRow(0)
                self.delete_this_alarm()
                self.player_mus = Player_music.MyWidget()
                self.player_mus.show()
        if self.flag:
            self.now_all_time = int(self.seconds.value()) + \
                                int(self.minutes.value()) * SECONDS + \
                                int(self.hours.value()) * SECONDS * SECONDS - 1
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
                self.player_mus = Player_music.MyWidget()
                self.player_mus.show()
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

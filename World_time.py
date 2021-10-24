import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer
qss = """
#my_timer {
    border-image: url(sky-sunset-night-star-atmosphere-twilight-galaxy-trees-stars-milkyway-coucherdesoleil-up-milchstrase-crpuscule.jpg) 0 0 0 0 stretch stretch;
}
"""


class Time(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Time.ui', self)
        self.setWindowTitle('AppClock')
        self.flag = False
        self.sec = 0
        self.min = 0
        self.msec = 0
        self.last = 0
        self.flag_two = False
        self.timer = QTimer(self)
        self.up_time = QTime(00, 00, 00)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()
        self.start.clicked.connect(self.countdown)
        self.reset.clicked.connect(self.restart)
        self.stop.clicked.connect(self.stopping)
        self.start_stopwatch.clicked.connect(self.starting)
        self.interval.clicked.connect(self.add_interval)
        self.total = 1
        self.list_times.addItem(f'Сircle            Total time             Lap time')
        self.list_times.addItem(f'--------------------------------------------------')

    def add_interval(self):
        now_time = int(self.stopwatch_l.text().split(":")[0]) * 100 + \
                   int(self.stopwatch_l.text().split(":")[1])
        dif = now_time - self.last
        if now_time - self.last < 1000:
            difference = '0'
        else:
            difference = ''
        if now_time - self.last < 10:
            difference_sec = '0'
        else:
            difference_sec = ''
        self.list_times.addItem(f'{self.total}{" " * 21}{self.stopwatch_l.text()}{" " * 19}'
                                f'{(difference + str(dif // 100)) + ":" + difference_sec + str(dif)}')
        self.total += 1
        self.last = now_time

    def starting(self):
        self.flag_two = True

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
                            int(self.minutes.value()) * 60 + int(self.hours.value()) * 3600
            if self.all_time != 0:
                self.difference = 100 // self.all_time
            else:
                self.flag = False

    def show_time(self):
        now_time = QTime.currentTime()
        text = now_time.toString('hh:mm:ss')
        self.time.setText(text)
        self.time_m.setText(text[0:5])
        self.time_l.setText(str(int(text[0:2]) - 2) + ':' + text[3:5])
        self.time_ny.setText(str(int(text[0:2]) - 7) + ':' + text[3:5])
        if self.flag_two:
            new_text = self.up_time.toString('hh:mm:ss')
            self.stopwatch_l.setText(f'{new_text[3:5]}:{new_text[6:8]}')
            self.up_time = self.up_time.addSecs(1)
        if self.flag:
            self.now_all_time = int(self.seconds.value()) + \
                                int(self.minutes.value()) * 60 + int(self.hours.value()) * 3600
            if self.now_all_time == 0:
                self.progressTime.setValue(100)
            else:
                self.progressTime.setValue(self.progressTime.value() +
                                           self.difference)
            self.seconds.setEnabled(False)
            self.minutes.setEnabled(False)
            self.hours.setEnabled(False)
            if self.seconds.value() != 0:
                self.seconds.setValue(int(self.seconds.value()) - 1)
            elif self.seconds.value() == 0 and self.minutes.value() != 0:
                self.seconds.setValue(59)
                self.minutes.setValue(int(self.minutes.value()) - 1)
            elif self.minutes.value() == 0 and self.hours.value() != 0:
                self.seconds.setValue(59)
                self.minutes.setValue(59)
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
    #app.setStyleSheet(qss)
    form = Time()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


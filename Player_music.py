import sys, constants, World_time

from PyQt5 import QtCore, QtMultimedia, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('player.ui', self)
        self.setWindowTitle('Signal')
        self.setGeometry((constants.SCREENSIZE[0] - 415) // 2, (constants.SCREENSIZE[1] - 600) // 2, 415, 108)
        self.load_mp3(constants.FNAME)
        self.time_widget = World_time.Time()
        self._closable = False
        self.flag = True
        self.left_seconds = 0
        self.left_minute = 0
        self.left_hours = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(constants.TIME_SET)
        self.show_time()
        self.stop.clicked.connect(self.player.stop)
        self.stop.clicked.connect(self.close_player)

    def closeEvent(self, event):
        if self._closable:
            super(MyWidget, self).closeEvent(event)
        else:
            event.ignore()

    def close_player(self):
        self.flag = False
        MyWidget().hide()
        self.hide()

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def show_time(self):
        if self.flag:
            self.player.play()
            self.left_seconds += 1
            if self.left_seconds > 59:
                self.left_minute += 1
                self.left_seconds %= 60
            if self.left_minute > 59:
                self.left_hours += 1
                self.left_minute %= 60
            self.time_left.setText(f'-{constants.len_object(self.left_hours)}:'
                                   f'{constants.len_object(self.left_minute)}:'
                                   f'{constants.len_object(self.left_seconds)}')
        else:
            self.left_seconds = 0
            self.left_minute = 0
            self.left_hours = 0
            self.player.stop()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(constants.QSS)
    window = MyWidget()
    # window.player.stop()
    window.setFixedSize(400, 160)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

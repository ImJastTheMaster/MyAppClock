import sys, Check_user, World_time

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import uic
qss = """
#widget {
    border-image: url(moon-sky.jpg) 0 0 0 0 stretch stretch;
}
#my_timer {
    border-image: url(sky.jpg) 0 0 0 0 stretch stretch;
}
#my_time {
    border-image: url(london-art.jpg) 0 0 0 0 stretch stretch;
}
"""


class Entrance(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('entranse_disain.ui', self)
        self.setWindowTitle('Entrance')
        screen = app.primaryScreen()
        size = screen.size()
        self.flag_pas = False
        self.flag_name = False
        self.password_add.setEchoMode(QLineEdit.Password)
        self.setGeometry((size.width() - 400) // 2, (size.height() - 500) // 2, 400, 500)
        self.name_add.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
        self.password_add.setValidator(QIntValidator())
        self.mask_btn.clicked.connect(self.enable)
        #self.close_app.clicked.connect(self.close_window())
        self.btn_name.clicked.connect(self.mask_name)
        self.regist.clicked.connect(self.go_to_app)

    def enable(self):
        if self.flag_pas:
            self.password_add.setEchoMode(QLineEdit.Password)
            self.flag_pas = False
        else:
            self.password_add.setEchoMode(QLineEdit.Normal)
            self.flag_pas = True

    def close_window(self):
        pass

    def mask_name(self):
        if self.flag_name:
            self.name_add.setEnabled(self.flag_name)
            self.flag_name = False
        else:
            self.name_add.setEnabled(self.flag_name)
            self.flag_name = True

    def go_to_app(self):
        if self.password_add.text() == '' or self.name_add.text() == '':
            return 0
        if Check_user.check(self.password_add.text(), self.name_add.text()):
            self.times = World_time.Time()
            self.times.setStyleSheet(qss)
            self.times.show()
            window.hide()
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    window = Entrance()
    window.show()
    sys.exit(app.exec_())
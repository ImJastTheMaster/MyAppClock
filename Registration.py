import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5 import uic
from PyQt5.QtCore import QRegExp
import World_time, Add_user, Entrance, constants


class MyError(Exception):
    def __init__(self, text):
        self.txt = text


class RegistrationUser(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Registration_Users.ui', self)
        self.setGeometry((constants.SCREENSIZE[0] - 350) // 2, (constants.SCREENSIZE[1] - 287) // 2, 350, 287)
        self.setWindowTitle('Registration')
        self.flag = False
        self.pas.setEchoMode(QLineEdit.Password)
        self.pas.setValidator(QIntValidator())
        self.mask_btn.clicked.connect(self.enable)
        self.registration.clicked.connect(self.save)
        self.initials = {"Password": '', "name": '', "surname": '', "patronymic": ''}
        self.name_add.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
        self.surname_add.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
        self.patronymic_add.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
        self.back.clicked.connect(self.close_window)

    def close_window(self):
        self.entrance = Entrance.EntranceApp()
        self.entrance.setStyleSheet(constants.QSS)
        self.entrance.setFixedSize(400, 500)
        self.entrance.show()
        RegistrationUser().hide()
        self.hide()

    def save(self):
        try:
            self.initials = {"Password": self.pas.text(), "name": self.name_add.text(),
                             "surname": self.surname_add.text(), "patronymic": self.patronymic_add.text()}
            if self.initials["Password"] == '' or self.initials["name"] == '' \
                    or self.initials["surname"] == '' \
                    or self.initials["patronymic"] == '':
                raise MyError('Not all fields are filled')
            self.error_label.setText('')
            if Add_user.get_result(self.initials["Password"], self.initials["name"],
                                   self.initials["surname"], self.initials["patronymic"]):
                self.times = World_time.Time()
                self.times.setStyleSheet(constants.QSS)
                self.times.setFixedSize(415, 557)
                self.times.show()
                RegistrationUser().hide()
                self.hide()
            else:
                self.error_label.setText('User already exists')
        except MyError as error:
            self.error_label.setText(str(error))

    def enable(self):
        if self.flag:
            self.pas.setEchoMode(QLineEdit.Password)
            self.flag = False
        else:
            self.pas.setEchoMode(QLineEdit.Normal)
            self.flag = True


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(constants.QSS)
    window = RegistrationUser()
    window.setFixedSize(350, 287)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
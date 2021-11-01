import sys, Check_user, World_time, Registration, constants, function_save

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import uic
# первый фаил с которого начинается приложение


class MyError(Exception):
    def __init__(self, text):
        self.txt = text


class EntranceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('entranse_disain.ui', self)
        self.setWindowTitle('Entrance')
        self.flag_pas = False
        self.flag_name = False
        self.password_add.setEchoMode(QLineEdit.Password)
        self.setGeometry((constants.SCREENSIZE[0] - 400) // 2, (constants.SCREENSIZE[1] - 500) // 2, 400, 500)
        self.name_add.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
        self.password_add.setValidator(QIntValidator())
        self.mask_btn.clicked.connect(self.enable)
        self.close_app.clicked.connect(self.close_window)
        self.btn_name.clicked.connect(self.mask_name)
        self.come_in.clicked.connect(self.go_to_app)
        self.registration_user.clicked.connect(self.come_to_register)

    def come_to_register(self):
        # перехожу в виджет регистрации
        self.reg = Registration.RegistrationUser()
        self.reg.show()
        self.reg.setFixedSize(350, 287)
        EntranceApp().hide()
        self.hide()

    def enable(self):
        # делаю видимым или не видимым пароль
        if self.flag_pas:
            self.password_add.setEchoMode(QLineEdit.Password)
            self.flag_pas = False
        else:
            self.password_add.setEchoMode(QLineEdit.Normal)
            self.flag_pas = True

    def close_window(self):
        # закрываю приложение если решил выйти
        EntranceApp().close()
        self.close()

    def mask_name(self):
        # маскирую имя
        if self.flag_name:
            self.name_add.setEnabled(self.flag_name)
            self.flag_name = False
        else:
            self.name_add.setEnabled(self.flag_name)
            self.flag_name = True

    def go_to_app(self):
        # перехожу в приложение если данные пользователя верны
        try:
            if self.password_add.text() == '' or self.name_add.text() == '':
                raise MyError('Not all fields are filled')
            if Check_user.check(self.password_add.text(), self.name_add.text()) is False:
                raise MyError('This user does not exist')
            if Check_user.check(self.password_add.text(), self.name_add.text()):
                function_save.save(function_save.check_admin(self.password_add.text(), self.name_add.text()))
                self.times = World_time.Time()
                self.times.setStyleSheet(constants.QSS)
                self.times.setFixedSize(415, 557)
                self.times.show()
                EntranceApp().hide()
                self.hide()
        except MyError as error:
            self.errors.setText(str(error))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(constants.QSS)
    window = EntranceApp()
    window.setFixedSize(400, 500)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

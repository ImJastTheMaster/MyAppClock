import sys, csv

from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
import World_time


class MyError(Exception):
    def __init__(self, text):
        self.txt = text


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.all_users = []
        screen = app.primaryScreen()
        size = screen.size()
        self.setGeometry((size.width() - 350) // 2, (size.height() - 287) // 2, 350, 287)
        self.setWindowTitle('Entrance')
        self.flag = False
        self.pas = QLineEdit(self)
        self.pas.setPlaceholderText("password")
        self.pas.setStyleSheet('background : #f0f0f0; font-weight: 500; color: rgb(0, 0, 0); font-size:10pt;')
        self.pas.setEchoMode(QLineEdit.Password)
        self.pas.setValidator(QIntValidator())
        self.pas.resize(150, 25)
        self.pas.move(125, 172)
        self.mask_btn = QPushButton('👁', self)
        self.mask_btn.resize(25, 25)
        self.mask_btn.move(276, 172)
        self.mask_btn.clicked.connect(self.enable)
        self.text = QLabel('Password:', self)
        self.text.move(30, 175)
        self.text.setStyleSheet("QLabel{font-size: 12pt;}")
        self.registration = QPushButton("Registration", self)
        self.registration.setStyleSheet('font-size:10pt')
        self.registration.resize(150, 25)
        self.registration.move(28, 232)
        self.registration.clicked.connect(self.save)
        self.error_label = QLabel(self)
        self.error_label.resize(200, 25)
        self.error_label.move(30, 200)
        heigth = 32
        self.texts = []
        self.initials = {"Password": '', "name": '', "surname": '', "patronymic": ''}
        for num, i in enumerate(['name', "surname", "patronymic"]):
            self.i = QLineEdit(self)
            self.texts.append((i, self.i))
            self.i.setPlaceholderText(i)
            self.i.setValidator(QRegExpValidator(QRegExp("[a-zA-Zа-яА-Я .,]{20}")))
            self.i.setStyleSheet('background : #f0f0f0; font-weight: 500; color: rgb(0, 0, 0); font-size:10pt;')
            self.i.resize(150, 25)
            self.i.move(125, heigth)
            self.num = QLabel(i[0].upper() + i[1::] + ': ', self)
            self.num.setStyleSheet("QLabel{font-size: 12pt;}")
            self.num.move(30, heigth)
            heigth += 40

    def save(self):
        try:
            for name, i in self.texts:
                self.initials[name] = i.text()
            self.initials["Password"] = self.pas.text()
            if self.initials["Password"] == '' or self.initials["name"] == '' \
                    or self.initials["surname"] == '' \
                    or self.initials["patronymic"] == '':
                raise MyError('GG')
            self.error_label.setText('')
            with open('file.csv', encoding="utf8") as r_file:
                reader = csv.DictReader(r_file, delimiter=';', quotechar='"')
                for i in reader:
                    self.all_users.append(i)
            with open('file.csv', 'w', newline='') as w_file:
                writer = csv.DictWriter(
                    w_file, fieldnames=list(self.initials.keys()), delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                self.all_users.append(self.initials)
                for i in self.all_users:
                    writer.writerow(i)
            self.times = World_time.Time()
            self.times.show()
            window.hide()
            self.hide()
        except MyError:
            self.error_label.setText('Not all fields are filled')
            self.error_label.setStyleSheet('color: rgb(255, 0, 0); font-size:12pt')

    def enable(self):
        if self.flag:
            self.pas.setEchoMode(QLineEdit.Password)
            self.flag = False
        else:
            self.pas.setEchoMode(QLineEdit.Normal)
            self.flag = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec_())

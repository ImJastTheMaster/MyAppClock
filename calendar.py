import sys, datetime, function_save, sqlite3, World_time
from Project import constants

from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QInputDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime, QTimer


class MyError(Exception):
    def __init__(self, text):
        self.txt = text


class DiaryEvents():
    def __init__(self, datetime, title):
        self.datetime = datetime
        self.title = title

    def to_print(self):
        return "{} - {}".format(self.datetime, self.title)

    def __str__(self):
        return self.to_print()


class MyCalendar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('plans.ui', self)
        self.setWindowTitle('Минипланировщик')
        self.setGeometry((constants.SCREENSIZE[0] - 805) // 2, (constants.SCREENSIZE[1] - 600) // 2, 805, 600)
        self.events = []
        self.all_events = []
        self.timeEdit.setMinimumTime(QTime.currentTime())
        self.calendarWidget.setMinimumDate(QDate.currentDate())
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(constants.TIME_SET)
        self.show_time()
        self.color = ''
        self.color_settings = ['', '']
        self.label_errors.hide()
        self.add_event.clicked.connect(self.run)
        if function_save.admin is False:
            self.return_color.hide()
            self.admin_color_btn.hide()
            self.admin_font.hide()
            self.list_alarms.resize(311, 542)
        self.admin_color_btn.clicked.connect(self.color_select)
        self.return_color.clicked.connect(self.back_color)
        self.admin_font.clicked.connect(self.set_font)
        self.select_alarms.clicked.connect(self.selection)
        self.delete_event.clicked.connect(self.delete_select_event)

    def delete_select_event(self):
        try:
            events = [self.list_alarms.item(i).text() for i in range(self.list_alarms.count())]
            select_event = self.list_alarms.selectedItems()[0].text()
            self.list_alarms.clear()
            self.all_events = []
            index_delete = constants.NOT_INDEX
            for i in events:
                if i != select_event:
                    self.list_alarms.addItem(i)
                    self.all_events.append(i)
                if str(i) == str(select_event):
                    index_delete = events.index(i)
            if index_delete != constants.NOT_INDEX:
                del self.events[index_delete]
            self.label_errors.setText('')
        except IndexError:
            self.label_errors.setText('No alarm selected')

    def selection(self):
        try:
            if self.list_alarms.count() == 0:
                self.time_widget = World_time.Time()
                self.time_widget.all.setCurrentWidget(self.time_widget.my_alarm)
                self.time_widget.show()
                self.time_widget.setFixedSize(415, 557)
                MyCalendar().hide()
                self.hide()
                return 0
            if function_save.user_id == 0:
                self.label_errors.show()
                raise MyError('Not id user')
            con = sqlite3.connect('AppClock_users_db.db')
            cur = con.cursor()
            for i in range(self.list_alarms.count()):
                flag = True
                alarms = cur.execute(f"""SELECT alarm 
                FROM Dates WHERE UserId = '{function_save.user_id}'""").fetchall()
                for j in alarms:
                    if j[0][0:20] == self.list_alarms.item(i).text()[0:20]:
                        cur.execute(f"""UPDATE Dates
                        SET alarm = '{self.list_alarms.item(i).text()}'
                        WHERE alarm = '{j[0]}'""")
                        flag = False
                if flag:
                    cur.execute(f"""INSERT INTO Dates(alarm, UserId)
                    VALUES('{self.list_alarms.item(i).text()}', '{function_save.user_id}')""")
            con.commit()
            con.close()
            self.time_widget = World_time.Time()
            self.time_widget.all.setCurrentWidget(self.time_widget.my_alarm)
            self.time_widget.show()
            self.time_widget.setFixedSize(415, 557)
            con = sqlite3.connect('AppClock_users_db.db')
            cur = con.cursor()
            self.time_widget.all_alarms.clear()
            for i in cur.execute(f"""SELECT alarm 
                                    FROM Dates WHERE UserId = '{function_save.user_id}'""").fetchall():
                self.time_widget.all_alarms.addItem(str(i[0]))
            self.time_widget.sort_alarm()
            MyCalendar().hide()
            self.hide()
        except MyError as error:
            self.label_errors.setText(str(error))

    def set_font(self):
        index, ok_pressed = QInputDialog.getItem(
            self, "Choose a font", "Fonts",
            ([str(i) for i in range(1, 17)]), 0, False)
        self.color_settings[1] = f'font: 75 {index}pt "MS Shell Dlg 2"'
        self.calendarWidget.setStyleSheet(self.color_settings[0] + ';' + self.color_settings[1])

    def back_color(self):
        self.calendarWidget.setStyleSheet('alternate-background-color: rgb(119, 136, 153);'
                                          'font: 75 16pt "MS Shell Dlg 2"; '
                                          'selection-background-color: rgb(119, 136, 153); '
                                          'gridline-color: rgb(0, 0, 0);')

    def color_select(self):
        colors = QColorDialog.getColor()
        if colors.isValid():
            self.color = "background-color: " + colors.name()
        self.color_settings[0] = self.color
        self.calendarWidget.setStyleSheet(self.color_settings[0] + ';' + self.color_settings[1])

    def run(self):
        time = datetime.datetime(self.calendarWidget.selectedDate().year(),
                                 self.calendarWidget.selectedDate().month(),
                                 self.calendarWidget.selectedDate().day(), self.timeEdit.time().hour(),
                                 self.timeEdit.time().minute())
        if self.add_alarm.text() == "":
            new_event = DiaryEvents(time, 'None')
        else:
            new_event = DiaryEvents(time, self.add_alarm.text())
        flag = True
        if new_event.to_print() not in self.all_events:
            for i in self.all_events:
                if new_event.to_print()[0:20] == i[0:20]:
                    self.events[self.all_events.index(i)] = new_event
                    self.all_events[self.all_events.index(i)] = new_event.to_print()
                    flag = False
                    break
            if flag:
                self.events.append(new_event)
                self.all_events.append(new_event.to_print())
            self.events = sorted(self.events, key=lambda x: x.datetime)
            self.list_alarms.clear()
            self.list_alarms.addItems([i.to_print() for i in self.events])

    def show_time(self):
        self.timeEdit.setMinimumTime(QTime.currentTime())
        self.calendarWidget.setMinimumDate(QDate.currentDate())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyCalendar()
    window.setFixedSize(805, 600)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
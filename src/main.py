import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidget,QTableWidgetItem, QHeaderView, QWidget
from PyQt5.QtCore import QRect
from math import sqrt
from utils.back import *
from datetime import datetime

from forms.mainwindow_ui import *
from forms.printwindow_ui import *

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.radioButton.setChecked(True)
        self.radioButton_11.setChecked(True)
        self.info = QMessageBox()
        self.info.setWindowTitle("Уведомление")

        self.warning = QMessageBox()
        self.warning.setIcon(QMessageBox.Critical)
        self.warning.setWindowTitle("Ошибка")

        self.tableWidget = QTableWidget()
        self.tableWidget.setGeometry(QRect(60, 30, 500, 500))
        self.tableWidget.setWindowTitle("Результат запроса")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7]
        self.radioButtons = [self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4, self.radioButton_5,
                    self.radioButton_6, self.radioButton_11, self.radioButton_12, self.radioButton_13, self.radioButton_14, self.radioButton_15]

        self.lineEdits = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5,self.lineEdit_6,self.lineEdit_7]
        self.pushButton.clicked.connect(self.func)
        # self.pushButton_2.clicked.connect(self.more_avg)

        self.radio()

        for rad in self.radioButtons:
            rad.clicked.connect(self.radio)

    def more_avg(self):
        self.con = create_session()
        try:
            lim = self.read_pos(self.lineEdit_8, self.label_10.text())
            skip = self.read_pos(self.lineEdit_9, self.label_9.text())
        except:
            return
        try:
            data = get_more_avg(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        except Exception as e:
            print(e)
        self.con.close()
        fill_table1(self.tableWidget, data, ["Id студента", "ФИО", "Id проекта", "Количество источников"])

    def func(self):
        widget = None
        self.con = create_session()
        if self.radioButton.isChecked():
            head = ["Id", "Номер группы", "Факультет", "Квалификация", "Год создания"]
            if self.radioButton_11.isChecked():
                self.get_groups(head)
            elif self.radioButton_12.isChecked():
                self.get_group1(head)
            elif self.radioButton_13.isChecked():
                self.create_group(head)
            elif self.radioButton_14.isChecked():
                self.update_group(head)
            else:
                self.delete_group()

        elif self.radioButton_2.isChecked():
            head = ["Id", "ФИО", "Id группы", "Номер зачетки", "Дата рождения", "Год поступления"]
            if self.radioButton_11.isChecked():
                self.get_students(head)
            elif self.radioButton_12.isChecked():
                self.get_student(head)
            elif self.radioButton_13.isChecked():
                self.create_student(head)
            elif self.radioButton_14.isChecked():
                self.update_student(head)
            else:
                self.delete_student()

        elif self.radioButton_3.isChecked():
            head = ["Id", "Название", "Сложность", "Год первой реализации"]
            if self.radioButton_11.isChecked():
                self.get_themes(head)
            elif self.radioButton_12.isChecked():
                self.get_theme(head)
            elif self.radioButton_13.isChecked():
                self.create_theme(head)
            elif self.radioButton_14.isChecked():
                self.update_theme(head)
            else:
                self.delete_theme()

        elif self.radioButton_4.isChecked():
            head = ["Id", "Название", "Тип", "Авторы", "Год издания"]
            if self.radioButton_11.isChecked():
                self.get_sources(head)
            elif self.radioButton_12.isChecked():
                self.get_source(head)
            elif self.radioButton_13.isChecked():
                self.create_source(head)
            elif self.radioButton_14.isChecked():
                self.update_source(head)
            else:
                self.delete_source()

        elif self.radioButton_5.isChecked():
            head = ["Id", "Id темы", "Id студента", "Оценка", "Дата сдачи"]
            if self.radioButton_11.isChecked():
                self.get_projects(head)
            elif self.radioButton_12.isChecked():
                self.get_project(head)
            elif self.radioButton_13.isChecked():
                self.create_project(head)
            elif self.radioButton_14.isChecked():
                self.update_project(head)
            else:
                self.delete_project()
        
        else:
            head = ["Id", "Id источника", "Id проекта"]
            if self.radioButton_11.isChecked():
                self.get_relations(head)
            elif self.radioButton_12.isChecked():
                self.get_relation(head)
            elif self.radioButton_13.isChecked():
                self.create_relation(head)
            elif self.radioButton_14.isChecked():
                self.update_relation(head)
            else:
                self.delete_relation()
        self.con.close()

    def get_relations(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_source_projects(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_relation(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_source_project(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_relation(self, header):
        values=[]
        try:
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
        except:
            return
        keys = ["source_id", "project_id"]

        try:
            data = create_source_project(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_relation(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
        except:
            return
        keys = ["source_id", "project_id"]

        try:
            data = update_source_project(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_relation(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_source_project(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")

    def get_projects(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_projects(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_project(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_project(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_project(self, header):
        values=[]
        try:
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_date(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["theme_id", "author_id", "mark", "passed"]

        try:
            data = create_project(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_project(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_date(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["theme_id", "author_id", "mark", "passed"]

        try:
            data = update_project(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_project(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_project(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")

    def get_sources(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_sources(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_source(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_source(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_source(self, header):
        values=[]
        try:
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_str(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_str(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_pos(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["name", "type", "authors", "creation"]

        try:
            data = create_source(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_source(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_str(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_str(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_pos(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["name", "type", "authors", "creation"]

        try:
            data = update_source(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_source(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_source(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")

    def get_themes(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_themes(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_theme(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_theme(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_theme(self, header):
        values=[]
        try:
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
        except:
            return
        keys = ["name", "complexity", "first_time"]

        try:
            data = create_theme(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_theme(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
        except:
            return
        keys = ["name", "complexity", "first_time"]

        try:
            data = update_theme(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_theme(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_theme(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")
        
    def get_students(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_students(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_student(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_student(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_student(self, header):
        values=[]
        try:
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_date(self.lineEdit_4, self.label_4.text()))
            values.append(self.read_pos(self.lineEdit_5, self.label_5.text()))
        except:
            return
        keys = ["fio", "group_id", "book_num", "birth", "enrollment"]

        try:
            data = create_student(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_student(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_str(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_pos(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_pos(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_date(self.lineEdit_4, self.label_4.text()))
            values.append(self.read_pos(self.lineEdit_5, self.label_5.text()))
        except:
            return
        keys = ["fio", "group_id", "book_num", "birth", "enrollment"]

        try:
            data = update_student(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_student(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_student(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")

    def radio(self):
        for i in self.lineEdits:
            i.clear()
        if self.radioButton.isChecked():
            self.set_labels(["Номер группы", "Факультет", "Квалификация", "Год создания", '', '', ''])
        elif self.radioButton_2.isChecked():
            self.set_labels(["ФИО", "Id группы", "Номер зачетки", "Дата рождения", 'Год поступления', '', ''])
        elif self.radioButton_3.isChecked():
            self.set_labels(["Название", "Сложность", "Год первой реализации", '', '', '', ''])
        elif self.radioButton_4.isChecked():
            self.set_labels(["Название", "Тип", "Авторы", "Год издания", '', '', ''])
        elif self.radioButton_5.isChecked():
            self.set_labels(["Id студента", "Id темы", "Оценка", "Дата сдачи", '', '', ''])
        else:
            self.set_labels(["Id источника", "Id проекта", '',  '', '', '', ''])

        if self.radioButton_11.isChecked():
            self.set_labels(['',  '', '', '', '',"Количество записей", "Количество пропущенных страниц"])
        elif self.radioButton_12.isChecked():
            self.set_labels(['',  '', '', '', '',"Id записи", ""])
        elif self.radioButton_13.isChecked():
            pass
        elif self.radioButton_14.isChecked():
            self.label_6.setText("Id записи")
        elif self.radioButton_15.isChecked():
            self.set_labels(["", "", '',  '', '', 'Id записи', ''])

    def set_labels(self, lst):
        for (i,lab) in enumerate(self.labels):
            lab.setText(lst[i])

    def get_groups(self, header):
        try:
            lim = self.read_pos(self.lineEdit_6, self.label_6.text())
            skip = self.read_pos(self.lineEdit_7, self.label_7.text())
        except:
            return
        try:
            data = get_all_groups(self.con, lim, skip)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, data, header)

    def get_group1(self, header):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = get_group(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        fill_table(self.tableWidget, [data], header)

    def create_group(self, header):
        values=[]
        try:
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_str(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_str(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_pos(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["group_num", "faculty", "qualification", "creation"]

        try:
            data = create_group(self.con, dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись добавлена")
        fill_table(self.tableWidget, [data], header)

    def update_group(self, header):
        values=[]
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
            values.append(self.read_pos(self.lineEdit_1, self.label_1.text()))
            values.append(self.read_str(self.lineEdit_2, self.label_2.text()))
            values.append(self.read_str(self.lineEdit_3, self.label_3.text()))
            values.append(self.read_pos(self.lineEdit_4, self.label_4.text()))
        except:
            return
        keys = ["group_num", "faculty", "qualification", "creation"]

        try:
            data = update_group(self.con, ID,dict(zip(keys, values)))
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        except Exception as e:
            self.show_warning(e.msg)
        self.show_info("Запись изменена")
        fill_table(self.tableWidget, [data], header)
    
    def delete_group(self):
        try:
            ID = self.read_pos(self.lineEdit_6, self.label_6.text())
        except:
            return
        try:
            data = delete_group(self.con, ID)
        except Exc as e:
            self.show_warning(e.msg)
            self.con.rollback()
            return
        self.show_info("Запись удалена")

    def read_pos(self, entry, name):
        try:
            value = int(entry.text())
            if value < 0:
                raise Exception()
            return value
        except:
            self.show_warning(f'В поле "{name}" должно быть целое значение')
            raise Exception()

    def read_date(self, entry, name):
        try:
            date = datetime.strptime(entry.text(), '%d.%m.%Y')
            return date
        except:
            self.show_warning(f'В поле "{name}" должна быть дата в формате DD.MM.YYYY')
            raise Exception()
            

    def read_str(self, entry, name):
        try:
            value = entry.text()
            if value == '':
                raise Exception()
            return value
        except:
            self.show_warning(f'В поле "{name}" должна быть непустая строка')
            raise Exception()
        
    def show_warning(self, msg):
        self.warning.setText(msg)
        self.warning.show()

    def show_info(self, msg):
        self.info.setText(msg)
        self.info.show()

def get_model_values(model):
    return list(model.__dict__.values())[1:]

def fill_table1(widget, data, header):
    widget.setRowCount(len(data))
    widget.setColumnCount(len(header))
    widget.setHorizontalHeaderLabels(header)
    data = [i[0][1:-1].split(',') for i in data]
    if len(data) > 0:
        for row in range(len(data)):
            for column in range(len(data[0])):
                    widget.setItem(row, column, QTableWidgetItem(str(data[row][column])))
    widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    widget.show()

def fill_table(widget, data, header):
    widget.setRowCount(len(data))
    widget.setColumnCount(len(header))
    widget.setHorizontalHeaderLabels(header)
    if len(data) > 0:
        for row in range(len(data)):
            for column in range(len(data[0])):
                    widget.setItem(row, column, QTableWidgetItem(str(data[row][column])))
    widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
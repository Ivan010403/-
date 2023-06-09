from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

import sqlite3
import sys
import gui

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = 'C://Users//vanyk//OneDrive//Рабочий стол//Учёба//ПИКПО//course.db'
        self.records = []
        self.initUI() 


    def initUI(self):
        wind = gui.Ui_MainWindow() 
        self.all_elements = wind.setupUi(self)
        
        self.all_elements[1].clicked.connect(self.extract_from_library)
        self.all_elements[2].clicked.connect(self.add_book)
        self.all_elements[3].clicked.connect(self.find_book)

        self.lines = wind.return_lines_edit()
        self.show()

        self.upload_data()

    def add_book(self):
        book = self.lines[1].text()
        author = self.lines[2].text()
        amount = self.lines[3].text()

        self.put_data_into_db(book, author, amount) 

    def extract_from_library(self):
        if len(self.lines[0].text()):
            self.delete_row(self.lines[0].text())

    def find_book(self):
        request = self.lines[4].text()

        temp = []
        count = 0

        for i in range(len(self.records)):
            if request == self.records[i][1] or request == self.records[i][2]:
                print(self.records[i])
                temp.append(self.records[i])
                count = count + 1
        
        print(temp)
        self.all_elements[0].setRowCount(len(temp))
        for i in range(len(temp)):
            self.all_elements[0].setItem(i, 0, QTableWidgetItem(str(temp[i][0])))
            self.all_elements[0].setItem(i, 1, QTableWidgetItem(temp[i][1]))
            self.all_elements[0].setItem(i, 2, QTableWidgetItem(temp[i][2]))
            self.all_elements[0].setItem(i, 3, QTableWidgetItem(str(temp[i][3])))



    def upload_data(self):
        sqlite_connection = sqlite3.connect(self.path)
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT * from books"""
        cursor.execute(sqlite_select_query)
        self.records = cursor.fetchall()

        self.all_elements[0].setRowCount(len(self.records))
        for i in range(len(self.records)):
            self.all_elements[0].setItem(i, 0, QTableWidgetItem(str(self.records[i][0])))
            self.all_elements[0].setItem(i, 1, QTableWidgetItem(self.records[i][1]))
            self.all_elements[0].setItem(i, 2, QTableWidgetItem(self.records[i][2]))
            self.all_elements[0].setItem(i, 3, QTableWidgetItem(str(self.records[i][3])))

    def update(self, id, book, author, amount):
        sqlite_connection = sqlite3.connect(self.path)
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update books set name = ? where id = ?"""
        data = (book, id)
        cursor.execute(sql_update_query, data)

        sql_update_query = """Update books set author = ? where id = ?"""
        data = (author, id)
        cursor.execute(sql_update_query, data)

        sql_update_query = """Update books set amount = ? where id = ?"""
        data = (amount, id)
        cursor.execute(sql_update_query, data)
        
        sqlite_connection.commit()

        self.upload_data()
        
    def put_data_into_db(self, book, author, amount):
        sqlite_connection = sqlite3.connect(self.path)
        cursor = sqlite_connection.cursor()

        id = len(self.records)+1

        for i in range(len(self.records)):
            if i + 1 !=self.records[i][0]:
                id = i + 1
                break

        sqlite_insert_query = """INSERT INTO books
                            (id, name, author, amount)
                            VALUES
                            (?, ?, ?, ?);"""
        
        data = (id, book, author, amount)
        cursor.execute(sqlite_insert_query, data)
        sqlite_connection.commit()

        self.upload_data()

    def delete_row(self, id):
        sqlite_connection = sqlite3.connect(self.path)
        cursor = sqlite_connection.cursor()

        for i in range(len(self.records)):
            if self.records[i][0] == int(id):
                if self.records[i][3] > 1:
                    self.update(self.records[i][0], self.records[i][1], self.records[i][2], self.records[i][3]-1)
                    return

        sql_delete_query = """DELETE from books where id = ?"""
        data = (id,)
        cursor.execute(sql_delete_query, data)

        sqlite_connection.commit()

        self.upload_data()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    app_1 = window()

    sys.exit(app.exec_())
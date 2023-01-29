import sys
import json
import mysql.connector
from PyQt5 import QtWidgets
from mysql.connector import Error, MySQLConnection
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QPlainTextEdit, QLineEdit, QLabel)

with open('users.json') as reader:
    users = json.load(reader)

gradient = QLinearGradient(0, 0, 0, 400)
gradient.setColorAt(0.8, QColor("#73C8A9"))
gradient.setColorAt(1.0, QColor("#474d59"))
p = QPalette()
p.setBrush(QPalette.Window, QBrush(gradient))
my_font = QFont('Bahnschrift Light', 15)
style_sheet_buttons = "QPushButton { background-color:#00b894;color:white;border-color:white;} " \
                      "QPushButton::hover { background-color:#00cec9;} QPushButton::pressed { background-color:#0984e3;}"
style_sheet_plain_text = "QPlainTextEdit {background-color:#636e72;color:white}"


class loginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Queries')
        self.setPalette(p)

        # -----------------------------                                  LOGIN PAGE                               --------------------------- #
        self.login_sign_up_layout = QGridLayout()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.login_sign_up_label = QLabel("")

        self.login_sign_up_user_list = QPlainTextEdit()
        self.login_sign_up_user_list.setReadOnly(True)
        self.login_sign_up_user_list.setPlaceholderText('Users')
        # ----------------------------------------------------------------------------------------------------------------------------------- #

        # -----------------------------                             STYLING LOGIN PAGE                           ---------------------------- #
        self.login_sign_up_layout.setVerticalSpacing(20)

        self.login_button.setFont(my_font)
        self.login_button.setMinimumHeight(35)
        self.login_button.setStyleSheet(style_sheet_buttons)
        self.login_sign_up_layout.addWidget(self.login_button, 0, 0)

        self.sign_up_button.setFont(my_font)
        self.sign_up_button.setMinimumHeight(35)
        self.sign_up_button.setStyleSheet(style_sheet_buttons)
        self.login_sign_up_layout.addWidget(self.sign_up_button, 1, 0)

        self.username.setFont(my_font)
        self.username.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.username, 2, 0)

        self.password.setFont(my_font)
        self.password.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.password, 3, 0)

        self.login_sign_up_label.setFont(my_font)
        self.login_sign_up_label.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.login_sign_up_label, 4, 0)

        self.login_sign_up_user_list.setFont(my_font)
        self.login_sign_up_user_list.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.login_sign_up_user_list, 5, 0)
        # ----------------------------------------------------------------------------------------------------------------------------------- #

        self.setLayout(self.login_sign_up_layout)

        # -----------------------------                                   BUTTON FUNCTIONS                             -------------------------- #

    def login(self):
        global connection
        global widget
        username = self.username.text()
        password = self.password.text()
        if not users.get(username):
            self.login_sign_up_label.setText("User not found!")
        if users.get(username) != password:
            self.login_sign_up_label.setText("Wrong password!")
        else:
            try:
                connection = mysql.connector.connect(host='127.0.0.1', database='mobilestore', user=username, password=password)
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                if connection.is_connected():
                    self.username.clear()
                    self.password.clear()
                    widget.setCurrentIndex(1)
            except Error as e:
                print("Error while connecting to MySQL", e)
                self.login_sign_up_label.setText("Error while connecting to MySQL")


    def sign_up(self):
        global connection
        for user in users:
            self.login_sign_up_user_list.appendPlainText(user + "\n")
        username = self.username.text()
        password = self.password.text()
        if users.get(username):
            self.login_sign_up_label.setText("Username already exist!")
        else:
            users[username] = password
            try:
                connection = mysql.connector.connect(host='127.0.0.1', database='mobilestore', user='root', password=users.get('root'))
                cursor = connection.cursor()
                cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'127.0.0.1' IDENTIFIED BY '{password}'")
                cursor.execute(f"GRANT SELECT ON *.* TO '{username}'@'127.0.0.1'")
                connection.commit()
                cursor.close()
                connection.close()
                self.login_sign_up_label.setText("User created successfully")
            except Error as e:
                print("Error while connecting to MySQL", e)
                self.login_sign_up_label.setText("Error while connecting to MySQL")


class queryPage(QWidget):
    def __init__(self):
        super().__init__()


connection: MySQLConnection
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
loginPage = loginPage()
queryPage = queryPage()
widget.addWidget(loginPage)
widget.addWidget(queryPage)
widget.setFixedHeight(1000)
widget.setFixedWidth(900)
widget.show()
sys.exit(app.exec_())

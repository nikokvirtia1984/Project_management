import sys
# import openpyxl
import datetime
from datetime import date
import json
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.uic import loadUi
import random

from PyQt6.uic.properties import QtCore

year = date.today().year
month = date.today().month
day = date.today().day
date = QDate(year, month, day)


def connect_to_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as base:
            users = json.load(base)
    except FileNotFoundError:
        users = {}
    return users


def update_users(data):
    with open('users.json', 'w', encoding='utf=8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def connection_to_db():
    try:
        with open('database.json', 'r', encoding='utf-8') as database:
            clients = json.load(database)
    except FileNotFoundError:
        print('კლიენტების სია ცარიელია, გთხოვთ დაამატოთ.')
        clients = {}
    return clients


def update_database(data):
    with open('database.json', 'w', encoding='utf=8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def wrong_email_pass():
    msg = QMessageBox()
    msg.setWindowTitle('არასწორი მონაცემები')
    msg.setText('სახელი ან პაროლი არასწორია.')
    msg.exec()


def sign_up_dialog():
    createacc = CreateAcc()
    widget.addWidget(createacc)
    widget.setFixedWidth(480)
    widget.setFixedHeight(540)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def accountant_window():
    clients = connection_to_db()
    mainw = AccountantApp()
    widget.addWidget(mainw)
    widget.setFixedHeight(540)
    widget.setFixedWidth(1120)
    date = QDate(year, month, day)
    mainw.actual_date.setDate(date)
    mainw.deadline_visit_date.setDate(date)
    mainw.actual_visit_date.setDate(date)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def close_accountant_window():
    mainwindow = Login()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(480)
    widget.setFixedHeight(400)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def client_names():
    clients = connection_to_db()
    names = []
    try:
        for client in clients:
            names.append(client)
    except TypeError as te:
        print(te)
    return names


def sales_manager_window():
    sales_manager = SalesManager()
    widget.addWidget(sales_manager)
    widget.setFixedWidth(400)
    widget.setFixedHeight(200)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def sales_managers():
    users = connect_to_users()
    users_name = []

    for key, value in users.items():
        if value['position'] == 'გაყიდვების მენეჯერი':
            users_name.append(value['fullname'])
    return users_name


def add_client():
    add_client_wind = AddClient()
    widget.addWidget(add_client_wind)
    widget.setFixedWidth(635)
    widget.setFixedHeight(465)
    date = QDate(year, month, day)
    add_client_wind.visit_date.setDate(date)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def close_add_client_window():
    sales_manager = SalesManager()
    widget.addWidget(sales_manager)
    widget.setFixedWidth(400)
    widget.setFixedHeight(200)
    widget.setCurrentIndex(widget.currentIndex() + 1)


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.login_button.clicked.connect(self.login_function)
        self.create_acc.clicked.connect(sign_up_dialog)

    def login_function(self):
        positions = {'ხარჯთაღმრიცხველი': accountant_window, 'გაყიდვების მენეჯერი': sales_manager_window}  # აქ ფუნქცია
        # იწერება () გარეშე
        users = connect_to_users()
        email = self.login.text()
        password = self.password.text()
        # ვამოწმებთ არის თუ არა იუზერი ბაზაში
        if email in users:
            # ვამოწმებთ პაროლს
            if email == users[email]['email'] and password == users[email]['password']:
                # ვიძახებთ ლექსიკონიდან იუზერის პოზიციის შესაბამის ფუნქციას ()-ით ბოლოში
                positions[users[email]['position']]()
            else:
                wrong_email_pass()
        else:
            wrong_email_pass()


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("signup_form.ui", self)
        self.sign_up.clicked.connect(self.create_acc_func)

    def create_acc_func(self):
        add_user = connect_to_users()
        fullname = self.name.text()
        email = self.login.text()
        phonenumber = self.phone_number.text()
        position = self.user_position.currentText()
        if email in add_user:
            QMessageBox.information(self, 'შეცდომა', 'ასეთი მომხმარებელი უკვე არსებობს, სცადეთ სხვა ელ-ფოსტა.',
                                    QMessageBox.StandardButton.Ok)
            sign_up_dialog()
        if self.password.text() == self.conf_pass.text():
            password = self.password.text()
            add_user[email] = {
                'fullname': fullname,
                'email': email,
                'phonenumber': phonenumber,
                'position': position,
                'password': password
            }
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        update_users(add_user)


class SalesManager(QMainWindow):
    def __init__(self):
        super(SalesManager, self).__init__()
        loadUi('sales_manager.ui', self)
        self.add_client_action.triggered.connect(add_client)


class AddClient(QMainWindow):
    def __init__(self):
        super(AddClient, self).__init__()
        loadUi('add_client.ui', self)
        self.sales_manager.addItems(sales_managers())
        self.add_client.clicked.connect(self.add)
        self.close_button.clicked.connect(close_add_client_window)

    def add(self):
        existing_client_id = random.randint(1, 50)
        clients = connection_to_db()
        contact_person = self.client_name.text()
        if contact_person in clients:
            contact_person = f"{contact_person}_{existing_client_id}"
        visit_date = self.visit_date.text()
        visit_date_obj = datetime.datetime.strptime(visit_date, "%d/%m/%Y")
        visit_deadline = datetime.datetime.strftime(visit_date_obj + datetime.timedelta(days=3), "%d/%m/%Y")

        clients[contact_person] = {
            'visit_date': self.visit_date.text(),
            'manager': self.sales_manager.currentText(),
            'address': self.address.text(),
            'type_of_work': self.work_type.currentText(),
            'cadastre_code': self.code.text(),
            'contact_person': contact_person,
            'phone': self.phone.text(),
            'building_type': self.building_type.currentText(),
            "visit_deadline": visit_deadline,
            "actual_visit_date": "",
            "time_status_red_description": "",
            "object_condition": "",
            "object_measurements": 0.0,
            "calculation_deadline": "",
            "calculation_actual_end_date": "",
            "calculation_status_red_description": "",
            "unit_price_in_gel": 0.0,
            "unit_price_in_usd": 0.0,
            "total_price_in_gel": 0.0,
            "potential_client_visit_in_office_date_deadline": "",
            "visit_actual_date": "",
            "if_status_red_description": "",
            "decision": "",
            "if_decision_no_description": "",
            "send_documentation_to_lawyer_date": "",
            "contract_preparation_deadline": "",
            "actual_preparation_date": "",
            "if_document_status_red_description": "",
            "status": ""
        }
        update_database(clients)
        self.client_name.setText('')
        self.address.setText('')
        self.code.setText('')
        self.phone.setText('')
        QMessageBox.information(self, 'კლიენტი დაემატა', f"კლიენტი '{contact_person}' წარმატებით დაემატა.",
                                QMessageBox.StandardButton.Ok)


class AccountantApp(QMainWindow):
    def __init__(self):
        super(AccountantApp, self).__init__()
        loadUi('accountant.ui', self)
        self.updateinfo.clicked.connect(self.accountant)
        self.close_button.clicked.connect(close_accountant_window)
        self.updateinfo.clicked.connect(self.update_client_information)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 80)
        self.client_list()
        self.unitpriceingel.textChanged.connect(lambda: self.calculate_total_price())
        # self.client_list_button.clicked.connect(self.client_list)
        self.tableWidget.cellClicked.connect(self.get_current_cell_value)
        self.deadline_date.setDate(date)
        # self.btn = QPushButton(self.tableWidget)
        # self.btn.setText('განახლება')
        self.clients = connection_to_db()
        # self.visit_deadline = self.clients[]
        # self.visit_deadline = datetime.datetime.strptime(clients[client_name]['visit_date'], '%d/%m/%Y') \
        # + datetime.timedelta(days=3)

    def accountant(self):
        pass
        # visit_deadline = datetime.datetime.strptime(clients[client_name]['visit_date'], '%d/%m/%Y') \
        #                   + datetime.timedelta(days=3)
        # print(f'დედლაინით განსაზღვრული ვიზიტის დრო: {visit_deadline.date().strftime("%d/%m/%Y")}')
        # clients[client_name]['visit_deadline'] = visit_deadline.date().strftime('%d/%m/%Y')
        # clients[client_name]['actual_visit_date'] = input('ფაქტობრივი ვიზიტის დრო: ')
        # actual_date = clients[client_name]['actual_visit_date']
        # actual = datetime.datetime.strptime(actual_date, '%d/%m/%Y')
        # if actual > visit_deadline:
        #     print(f'დაგვიანება: {str(actual - visit_deadline)[0:1]} დღე.')
        #     clients[client_name]['time_status_red_description'] = input('ჩაწერეთ დაგვიანების მიზეზი: ')
        # else:
        #     clients[client_name]['time_status_red_description'] = ' '
        # clients[client_name]['object_condition'] = input('ობიექტის მდგომარობა (თეთრი კარკასი; შავი კარკასი; '
        #                                                  'მონოლითური და სხვა): ')
        # clients[client_name]['object_measurements'] = self.mesurement.text()
        # calculation_deadline = visit_deadline + datetime.timedelta(days=5)
        # print(f'დედლაინით განსაზღვრული ხარჯთაღრიცხვის დასრულების დრო: {calculation_deadline.strftime("%d/%m/%Y")}')
        # clients[client_name]['calculation_deadline'] = calculation_deadline.date().strftime('%d/%m/%Y')
        # clients[client_name]['calculation_actual_end_date'] = input('ფაქტობრივი დასრულების თარიღი: ')
        # calc_actual_date = clients[client_name]['calculation_actual_end_date']
        # calc_actual = datetime.datetime.strptime(calc_actual_date, '%d/%m/%Y')
        # if calc_actual > calculation_deadline:
        #     print(f'დაგვიანება: {str(calc_actual - calculation_deadline)[0:1]} დღე.')
        #     clients[client_name]['calculation_status_red_description'] = input('შენიშვნა ვადაგადაცილების '
        #                                                                        'შემთხვევაში: ')
        # else:
        #     clients[client_name]['calculation_status_red_description'] = ' '
        # clients[client_name]['unit_price_in_gel'] = self.unitpriceingel.text()
        # clients[client_name]['unit_price_in_usd'] = round(clients[client_name]['unit_price_in_gel'] / 3.1, 2)
        # clients[client_name]['total_price_in_gel'] = clients[client_name]['unit_price_in_gel'] * \
        #                                              clients[client_name]['object_measurements']

        # update_database(clients)

    def client_list(self):
        clients = connection_to_db()
        row = 0
        self.tableWidget.setHorizontalHeaderLabels(['კლიენტის სახელი', 'ტელეფონი'])
        self.tableWidget.setRowCount(len(clients))
        for client in clients:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(client))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(clients[client]["phone"])))
            # self.tableWidget.setCellWidget(row, 2, self.btn)

            row += 1


    def calculate_deadline(self):
        deadline_date = self.actual_visit_date.date().addDays(5)
        self.deadline_date.setDate(deadline_date)

    def calculate_total_price(self):
        client_name = self.client_name_text.text()
        total_price = float(self.measurement.text()) * float(self.unitpriceingel.text())
        self.total_price.setText(str(total_price))

    def get_current_cell_value(self):
        current_row = self.tableWidget.currentRow()
        client_name = str(self.tableWidget.item(current_row, 0).text())
        self.client_name_text.setText(client_name)
        self.deadline_visit_date.setDate(QDate.fromString(self.clients[client_name]['visit_deadline'], 'd/M/yyyy'))
        self.actual_visit_date.dateChanged.connect(lambda: self.calculate_deadline())
        self.object_condition.setCurrentText(self.clients[client_name]['object_condition'])
        self.measurement.setText(str(self.clients[client_name]['object_measurements']))
        self.unitpriceingel.setText(str(self.clients[client_name]['unit_price_in_gel']))
        self.unitpriceinusd.setText(str(self.clients[client_name]['unit_price_in_usd']))
        self.calculate_total_price()

    def update_client_information(self):
        clients = connection_to_db()
        client_name = self.client_name_text.text()
        clients[client_name]['actual_visit_date'] = self.actual_visit_date.text()
        clients[client_name]['object_condition'] = self.object_condition.currentText()
        clients[client_name]['object_measurements'] = float(self.measurement.text())
        clients[client_name]['calculation_deadline'] = self.deadline_date.text()
        clients[client_name]['calculation_actual_end_date'] = self.actual_date.text()
        clients[client_name]['unit_price_in_gel'] = float(self.unitpriceingel.text())
        clients[client_name]['unit_price_in_usd'] = float(self.unitpriceinusd.text())
        self.calculate_total_price()
        clients[client_name]['total_price_in_gel'] = float(self.total_price.text())

        update_database(clients)
        QMessageBox.information(self, 'ინფორმაციის განახლება', f"ინფორმაცია კლიენტზე '{client_name}' წარმატებით განახლდა.",
                        QMessageBox.StandardButton.Ok)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(400)
widget.show()
app.exec()

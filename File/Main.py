import sys

from PyQt6.QtGui import QPixmap

from db import db_con
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db_con.create_tables()

        self.main_layout = QHBoxLayout()
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        self.user_icon = QLabel()          #user icon
        user_img = QPixmap("user_icon.png")
        self.user_icon.setPixmap(user_img)
        self.user_greeting = QLabel("Hi, User")
        self.user_logo = QVBoxLayout()
        self.user_logo.addWidget(self.user_icon)
        self.user_logo.addWidget(self.user_greeting)

        self.main_tabs = QTabWidget()

        self.msds_tab = QWidget()            #MSDS Main Tab
        self.coa_tab = QWidget()            #MSDS Main Tab
        self.msds_layout = QVBoxLayout(self.msds_tab)
        self.coa_layout = QVBoxLayout(self.coa_tab)

        self.msds_sub_tabs = QTabWidget()     #Sub tabs
        self.msds_layout.addWidget(self.msds_sub_tabs)

        self.msds_data_entry_tab = QWidget()
        self.msds_data_entry_layout = QVBoxLayout(self.msds_data_entry_tab)
        self.msds_data_entry_layout.addWidget(QLabel("Data Entry"))

        self.msds_records_tab = QWidget()
        self.msds_records_layout = QVBoxLayout(self.msds_records_tab)
        self.msds_records_layout.addWidget(QLabel("Records"))

        self.coa_tab = QWidget()  # MSDS Main Tab
        self.coa_layout = QVBoxLayout(self.coa_tab)

        self.coa_sub_tabs = QTabWidget()  # Sub tabs
        self.coa_layout.addWidget(self.coa_sub_tabs)

        self.coa_data_entry_tab = QWidget()
        self.coa_data_entry_layout = QVBoxLayout(self.coa_data_entry_tab)
        self.coa_data_entry_layout.addWidget(QLabel("Data Entry"))

        self.coa_records_tab = QWidget()
        self.coa_records_layout = QVBoxLayout(self.coa_records_tab)
        self.coa_records_layout.addWidget(QLabel("Records"))

        self.msds_sub_tabs.addTab(self.msds_data_entry_tab, "Data Entry")
        self.msds_sub_tabs.addTab(self.msds_records_tab, "Records")

        self.coa_sub_tabs.addTab(self.coa_data_entry_tab, "Data Entry")
        self.coa_sub_tabs.addTab(self.coa_records_tab, "Records")


        self.main_tabs.addTab(self.msds_tab, "MSDS")
        self.main_tabs.addTab(self.coa_tab, "CoA")

        self.left_column.addLayout(self.user_logo)
        self.left_column.addWidget(self.main_tabs)

        self.main_layout.addLayout(self.left_column, 20)
        self.main_layout.addLayout(self.right_column, 80)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)





    def initUI(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Document Management System")
    window.resize(1000, 800)
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

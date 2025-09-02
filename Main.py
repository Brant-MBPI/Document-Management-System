import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from db import db_con
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem
import msds_data_entry
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db_con.create_tables()

        self.main_layout = QVBoxLayout()
        self.main_tabs = QTabWidget()

        self.section1_layout = QVBoxLayout()
        self.section2_layout = QVBoxLayout()
        self.section3_layout = QVBoxLayout()
        self.section4_layout = QVBoxLayout()
        self.section5_layout = QVBoxLayout()
        self.section6_layout = QVBoxLayout()
        self.section7_layout = QVBoxLayout()
        self.section8_layout = QVBoxLayout()


        # MSDS FORM init
            #Section 1
        self.trade_label_input = QLineEdit()
        self.manufactured_label_input = QLineEdit()
        self.tel_label_input = QLineEdit()
        self.facsimile_label_input = QLineEdit()
        self.email_label_input = QLineEdit()
            #Section2
        self.composition_input = QLineEdit()
            #Section3
        self.hazard_preliminaries_input = QLineEdit()
        self.hazard_entry_route_input = QLineEdit()
        self.hazard_symptoms_input = QLineEdit()
        self.hazard_restrictive_condition_input = QLineEdit()
        self.hazard_eyes_input = QLineEdit()
        self.hazard_general_note_input = QLineEdit()
            #Section4
        self.first_aid_inhalation_input = QLineEdit()
        self.first_aid_eyes = QLineEdit()
        self.first_aid_skin_input = QLineEdit()
        self.first_aid_ingestion_input = QLineEdit()
            #Section5
        self.fire_fighting_media_input = QLineEdit()
            #Section6
        self.accidental_release_input = QLineEdit()
            #Section7
        self.handling_input = QLineEdit()
        self.storage_input = QLineEdit()
            #Section8
        self.exposure_control_input = QLineEdit()
        self.respiratory_protection_input = QLineEdit()
        self.hand_protection_input = QLineEdit()
        self.eye_protection_input = QLineEdit()
        self.skin_protection_input = QLineEdit()



        self.msds_tab = QWidget()           #MSDS Main Tab
        self.msds_layout = QVBoxLayout(self.msds_tab)

        self.msds_sub_tabs = QTabWidget()
        self.msds_layout.addWidget(self.msds_sub_tabs)

        self.msds_data_entry_tab = QWidget()
        self.msds_records_tab = QWidget()

        self.coa_tab = QWidget()  # COA Main Tab
        self.coa_layout = QVBoxLayout(self.coa_tab)

        self.coa_sub_tabs = QTabWidget()
        self.coa_layout.addWidget(self.coa_sub_tabs)

        self.coa_data_entry_tab = QWidget()
        self.coa_records_tab = QWidget()

        # SUB-TAB
        self.msds_sub_tabs.addTab(self.msds_records_tab, "Records")
        self.msds_sub_tabs.addTab(self.msds_data_entry_tab, "Data Entry")

        self.coa_sub_tabs.addTab(self.coa_records_tab, "Records")
        self.coa_sub_tabs.addTab(self.coa_data_entry_tab, "Data Entry")

        self.main_tabs.addTab(self.msds_tab, "MSDS")
        self.main_tabs.addTab(self.coa_tab, "CoA")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")

        self.main_tabs.setCornerWidget(self.search_bar)

        self.msds_records_table = QTableWidget()   # MSDS Record Table
        self.msds_records_table.setColumnCount(4)
        self.msds_records_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.msds_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Override resize event
        self.msds_records_table.resizeEvent = self.resize_columns
        self.msds_records_table.verticalHeader().setDefaultSectionSize(40)
        self.msds_records_table.horizontalHeader().setFixedHeight(40)
        self.msds_records_table.setShowGrid(False)
        self.msds_records_table.setStyleSheet("""
            QTableWidget::item {
                border-right: none;
                border-bottom: 1px solid lightgray;
                padding-left: 10px;
                height: 36px;
            }
            QTableWidget::item:selected {
                background-color: #3399FF;           
                color: black;                         
            }
            QHeaderView::section {
                border-right: none;                  
                border-bottom: 1px solid lightgray; 
                background-color: #f0f0f0;         
            }
        """)

        self.msds_records_layout = QVBoxLayout(self.msds_records_tab)  # inside MSDS sub-tab Records
        self.msds_records_layout.addWidget(self.msds_records_table)

        self.msds_data_entry_layout = QVBoxLayout(self.msds_data_entry_tab)  # inside MSDS sub-tab Data Entry
        self.msds_data_entry_layout.addLayout(self.section1_layout)
        self.msds_data_entry_layout.addLayout(self.section2_layout)
        self.msds_data_entry_layout.addLayout(self.section3_layout)
        self.msds_data_entry_layout.addLayout(self.section4_layout)
        self.msds_data_entry_layout.addLayout(self.section5_layout)
        self.msds_data_entry_layout.addLayout(self.section6_layout)
        self.msds_data_entry_layout.addLayout(self.section7_layout)
        self.msds_data_entry_layout.addLayout(self.section8_layout)

        self.coa_records_layout = QVBoxLayout(self.coa_records_tab)  # inside COA sub-tab Records
        self.coa_records_layout.addWidget(QLabel("Records"))

        self.coa_data_entry_layout = QVBoxLayout(self.coa_data_entry_tab)  # inside COA sub-tab Data Entry
        self.coa_data_entry_layout.addWidget(QLabel("Data Entry"))

        self.main_layout.addWidget(self.main_tabs)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.load_msds_table()
        msds_data_entry.form_section1(self)
        msds_data_entry.form_section2(self)
        msds_data_entry.form_section3(self)
        msds_data_entry.form_section4(self)
        msds_data_entry.form_section5(self)
        msds_data_entry.form_section6(self)
        msds_data_entry.form_section7(self)
        msds_data_entry.form_section8(self)


    def load_msds_table(self):
        self.msds_records_table.insertRow(0)
        self.msds_records_table.setItem(0, 0, self.create_readonly_item("JDS WA17857E MSDS TDS 08-22-25"))
        self.msds_records_table.setItem(0, 1, self.create_readonly_item(icon_path="img/view_icon.png", selectable=False))
        self.msds_records_table.setItem(0, 2, self.create_readonly_item(icon_path="img/delete_icon.png", selectable=False))
        self.msds_records_table.setItem(0, 3, self.create_readonly_item(icon_path="img/print_icon.png", selectable=False))

    def resize_columns(self, event):
        total_width = self.msds_records_table.viewport().width()

        # first column = 70%
        first_col_width = int(total_width * 0.9)
        self.msds_records_table.setColumnWidth(0, first_col_width)

        # remaining columns share 30%
        remaining_width = total_width - first_col_width
        other_cols = self.msds_records_table.columnCount() - 1
        if other_cols > 0:
            each_width = int(remaining_width / other_cols)
            for col in range(1, self.msds_records_table.columnCount()):
                self.msds_records_table.setColumnWidth(col, each_width)

        super(QTableWidget, self.msds_records_table).resizeEvent(event)

    def create_readonly_item(self, text=None, icon_path=None, selectable=True):
        item = QTableWidgetItem()

        if text is not None:
            item.setText(text)

        if icon_path is not None:
            item.setIcon(QIcon(icon_path))

        # Make the item read-only
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        if not selectable:
            # Remove the selectable flag but keep enabled to accept clicks
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        return item


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Document Management System")
    window.resize(1000, 800)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

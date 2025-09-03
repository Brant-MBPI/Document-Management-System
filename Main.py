
import sys

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QIntValidator

import coa_data_entry
from db import db_con
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem, QScrollArea, QTextEdit, QPushButton, QDateEdit
import msds_data_entry
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # db_con.create_tables()

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
        self.section9_layout = QVBoxLayout()
        self.section10_layout = QVBoxLayout()
        self.section11_layout = QVBoxLayout()
        self.section12_layout = QVBoxLayout()
        self.section13_layout = QVBoxLayout()
        self.section14_layout = QVBoxLayout()
        self.section15_layout = QVBoxLayout()
        self.section16_layout = QVBoxLayout()
        self.section17_layout = QVBoxLayout()
        self.msds_btn_layout = QHBoxLayout()
        self.coa_btn_layout = QHBoxLayout()
        self.coa_form_layout = QVBoxLayout()

        # MSDS FORM init
            #Section 1
        self.trade_label_input = QLineEdit()
        self.manufactured_label_input = QTextEdit()
        self.tel_label_input = QLineEdit()
        self.facsimile_label_input = QLineEdit()
        self.email_label_input = QLineEdit()
            #Section2
        self.composition_input = QTextEdit()
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
        self.fire_fighting_media_input = QTextEdit()
            #Section6
        self.accidental_release_input = QTextEdit()
            #Section7
        self.handling_input = QLineEdit()
        self.msds_storage_input = QLineEdit()
            #Section8
        self.exposure_control_input = QLineEdit()
        self.respiratory_protection_input = QLineEdit()
        self.hand_protection_input = QLineEdit()
        self.eye_protection_input = QLineEdit()
        self.skin_protection_input = QLineEdit()
            #Section9
        self.appearance_input = QLineEdit()
        self.odor_input = QLineEdit()
        self.heat_stability_input = QLineEdit()
        self.light_fastness_input = QLineEdit()
        self.decomposition_input = QLineEdit()
        self.flash_point_input = QLineEdit()
        self.auto_ignition_input = QLineEdit()
        self.explosion_property_input = QLineEdit()
        self.solubility_input = QLineEdit()
            #Section10
        self.stability_reactivity_input = QTextEdit()
            #Section11
        self.toxicological_input = QTextEdit()
            #Section12
        self.ecological_input = QTextEdit()
            #Section13
        self.disposal_input = QTextEdit()
            #Section14
        self.transport_input = QTextEdit()
            #Section15
        self.regulatory_input = QTextEdit()
            #Section16
        self.msds_shelf_life_input = QTextEdit()
            #Section17
        self.other_input = QTextEdit()
            #Submit Button
        self.btn_msds_submit = QPushButton("Submit")

        # COA form init
            #summary of analysis table
        self.summary_analysis_table = QTableWidget()
            #inputs variable
        self.coa_customer_input = QLineEdit()
        self.color_code_input = QLineEdit()
        self.quantity_delivered_input = QLineEdit()
        self.delivery_date_input = QDateEdit()
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDate(QDate.currentDate())
        self.lot_number_input = QLineEdit()
        self.production_date_input = QDateEdit()
        self.production_date_input.setCalendarPopup(True)
        self.production_date_input.setDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1))
        self.delivery_receipt_input = QLineEdit()
        self.po_number_input = QLineEdit()
        self.certified_by_input = QLineEdit()
        self.creation_date_input = QDateEdit()
        self.creation_date_input.setCalendarPopup(True)
        self.creation_date_input.setDate(QDate.currentDate())
        self.coa_storage_input = QLineEdit()
        self.coa_shelf_life_input = QLineEdit()
        self.suitability_input = QLineEdit()
        self.btn_coa_submit = QPushButton   ("Submit")

        self.po_number_input.setValidator((QIntValidator(0, 2147483647)))

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

        self.msds_search_bar = QLineEdit()
        self.msds_search_bar.setPlaceholderText("Search...")
        self.coa_search_bar = QLineEdit()
        self.coa_search_bar.setPlaceholderText("Search...")

        self.msds_sub_tabs.setCornerWidget(self.msds_search_bar)
        self.coa_sub_tabs.setCornerWidget(self.coa_search_bar)

        self.msds_sub_tabs.currentChanged.connect(self.toggle_msds_search_bar)
        self.coa_sub_tabs.currentChanged.connect(self.toggle_coa_search_bar)

        self.msds_records_table = QTableWidget()   # MSDS Record Table

        self.msds_records_layout = QVBoxLayout(self.msds_records_tab)  # inside MSDS sub-tab Records
        self.msds_records_layout.addWidget(self.msds_records_table)

        scroll_area = QScrollArea(self.msds_data_entry_tab)
        scroll_area.setWidgetResizable(True)

        # Form container inside the scroll area
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)

        form_layout.addLayout(self.section1_layout)
        form_layout.addLayout(self.section2_layout)
        form_layout.addLayout(self.section3_layout)
        form_layout.addLayout(self.section4_layout)
        form_layout.addLayout(self.section5_layout)
        form_layout.addLayout(self.section6_layout)
        form_layout.addLayout(self.section7_layout)
        form_layout.addLayout(self.section8_layout)
        form_layout.addLayout(self.section9_layout)
        form_layout.addLayout(self.section10_layout)
        form_layout.addLayout(self.section11_layout)
        form_layout.addLayout(self.section12_layout)
        form_layout.addLayout(self.section13_layout)
        form_layout.addLayout(self.section14_layout)
        form_layout.addLayout(self.section15_layout)
        form_layout.addLayout(self.section16_layout)
        form_layout.addLayout(self.section17_layout)
        form_layout.addLayout(self.msds_btn_layout)

        scroll_area.setWidget(form_container)

        # Final layout for the tab
        self.msds_data_entry_layout = QVBoxLayout(self.msds_data_entry_tab)
        self.msds_data_entry_layout.addWidget(scroll_area)

        #Inside COA Records Tab
        self.coa_records_table = QTableWidget()

        self.coa_records_layout = QVBoxLayout(self.coa_records_tab)  # inside COA sub-tab Records
        self.coa_records_layout.addWidget(self.coa_records_table)



        self.coa_data_entry_layout = QVBoxLayout(self.coa_data_entry_tab)  # inside COA sub-tab Data Entry
        self.coa_data_entry_layout.addLayout(self.coa_form_layout)

        self.main_layout.addWidget(self.main_tabs)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        self.setStyleSheet(""" 
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
        self.msds_table_records_init()
        self.coa_table_records_init()
        self.load_msds_table()
        self.load_coa_table()
        coa_data_entry.coa_data_entry_form(self)

        msds_data_entry.form_section1(self)
        msds_data_entry.form_section2(self)
        msds_data_entry.form_section3(self)
        msds_data_entry.form_section4(self)
        msds_data_entry.form_section5(self)
        msds_data_entry.form_section6(self)
        msds_data_entry.form_section7(self)
        msds_data_entry.form_section8(self)
        msds_data_entry.form_section9(self)
        msds_data_entry.form_section10(self)
        msds_data_entry.form_section11(self)
        msds_data_entry.form_section12(self)
        msds_data_entry.form_section13(self)
        msds_data_entry.form_section14(self)
        msds_data_entry.form_section15(self)
        msds_data_entry.form_section16(self)
        msds_data_entry.form_section17(self)
        msds_data_entry.from_btn(self)


    def load_msds_table(self):
        self.msds_records_table.insertRow(0)
        self.msds_records_table.setItem(0, 0, self.create_readonly_item("JDS WA17857E MSDS TDS 08-22-25"))
        self.msds_records_table.setItem(0, 1, self.create_readonly_item(icon_path="img/view_icon.png", selectable=False))
        self.msds_records_table.setItem(0, 2, self.create_readonly_item(icon_path="img/delete_icon.png", selectable=False))
        self.msds_records_table.setItem(0, 3, self.create_readonly_item(icon_path="img/print_icon.png", selectable=False))

    def load_coa_table(self):
        self.coa_records_table.insertRow(0)
        self.coa_records_table.setItem(0, 0, self.create_readonly_item("JDS WA17857E MSDS TDS 08-22-25"))
        self.coa_records_table.setItem(0, 1, self.create_readonly_item(icon_path="img/view_icon.png", selectable=False))
        self.coa_records_table.setItem(0, 2, self.create_readonly_item(icon_path="img/delete_icon.png", selectable=False))
        self.coa_records_table.setItem(0, 3, self.create_readonly_item(icon_path="img/print_icon.png", selectable=False))

    def resize_columns(self, table: QTableWidget, event):
        total_width = table.viewport().width()

        # first column = 90%
        first_col_width = int(total_width * 0.9)
        table.setColumnWidth(0, first_col_width)

        # remaining columns share 10%
        remaining_width = total_width - first_col_width
        other_cols = table.columnCount() - 1
        if other_cols > 0:
            each_width = int(remaining_width / other_cols)
            for col in range(1, table.columnCount()):
                table.setColumnWidth(col, each_width)
        super(QTableWidget, table).resizeEvent(event)

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

    def msds_table_records_init(self):
        self.msds_records_table.setColumnCount(4)
        self.msds_records_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.msds_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Override resize event
        self.msds_records_table.resizeEvent = lambda event: self.resize_columns(self.msds_records_table, event)
        self.msds_records_table.verticalHeader().setDefaultSectionSize(40)
        self.msds_records_table.verticalHeader().setFixedWidth(40)
        self.msds_records_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msds_records_table.horizontalHeader().setFixedHeight(40)
        self.msds_records_table.setShowGrid(False)

    def coa_table_records_init(self):
        self.coa_records_table.setColumnCount(4)
        self.coa_records_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.coa_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Override resize event
        self.coa_records_table.resizeEvent = lambda event: self.resize_columns(self.coa_records_table, event)
        self.coa_records_table.verticalHeader().setDefaultSectionSize(40)
        self.coa_records_table.verticalHeader().setFixedWidth(40)
        self.coa_records_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.coa_records_table.horizontalHeader().setFixedHeight(40)
        self.coa_records_table.setShowGrid(False)

    def toggle_msds_search_bar(self, index):
        if index == 0:  # Records tab
            self.msds_search_bar.show()
        else:  # Other tabs
            self.msds_search_bar.hide()

    def toggle_coa_search_bar(self, index):
        if index == 0:  # Records tab
            self.coa_search_bar.show()
        else:
            self.coa_search_bar.hide()
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Document Management System")
    window.resize(1000, 800)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

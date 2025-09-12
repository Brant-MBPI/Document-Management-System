from datetime import datetime
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QSizePolicy, QHeaderView, QPushButton, QInputDialog, QTableWidgetItem, \
    QFormLayout, QTableWidget, QLineEdit, QAbstractItemView, QWidget
from alert import window_alert
from db import db_con

current_coa_id = None  # Global variable to store the current COA ID

def load_coa_details(self, coa_id):
    field_result = db_con.get_single_coa_data(coa_id)
    analysis_table_result = db_con.get_coa_analysis_results(coa_id)

    # === Populate inputs ===
    self.coa_customer_input.setText(str(field_result[1]))
    self.color_code_input.setText(str(field_result[2]))
    self.lot_number_input.setText(str(field_result[3]))
    self.po_number_input.setText(str(field_result[4]))
    self.delivery_receipt_input.setText(str(field_result[5]))
    self.quantity_delivered_input.setText(str(field_result[6]))
    self.delivery_date_input.setDate(QDate(field_result[7].year, field_result[7].month, field_result[7].day))
    self.production_date_input.setDate(QDate(field_result[8].year, field_result[8].month, field_result[8].day))
    self.creation_date_input.setDate(QDate(field_result[9].year, field_result[9].month, field_result[9].day))
    self.certified_by_input.setText(str(field_result[10]))
    self.coa_storage_input.setText(str(field_result[11]))
    self.coa_shelf_life_input.setText(str(field_result[12]))
    self.suitability_input.setText(str(field_result[13]))
    self.btn_coa_submit.setText("Update")

    # === Populate table ===
    self.summary_analysis_table.clearContents()
    self.summary_analysis_table.setRowCount(len(analysis_table_result))
    self.summary_analysis_table.setColumnCount(2)
    self.summary_analysis_table.setHorizontalHeaderLabels(["Standard Value", "Delivery Value"])

    for row_idx, (parameter_name, standard_value, delivery_value) in enumerate(analysis_table_result):
        self.summary_analysis_table.setVerticalHeaderItem(row_idx, QTableWidgetItem(parameter_name))
        self.summary_analysis_table.setItem(row_idx, 0, QTableWidgetItem(str(standard_value) if standard_value else ""))
        self.summary_analysis_table.setItem(row_idx, 1, QTableWidgetItem(str(delivery_value) if delivery_value else ""))

    adjust_table_height(self)

def coa_data_entry_form(self):
    try:
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

        form_layout.setHorizontalSpacing(24)
        form_layout.setVerticalSpacing(18)
        form_layout.setContentsMargins(40, 40, 90, 40)

        form_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 15px;
                font-weight: 500;
                color: #333333;
                margin-left: 0;
            }
            QLabel[class="sub_title"] {
                font-size: 20px;
                font-weight: 600;
                color: #1a73e8;
                margin-top: 16px;
                margin-bottom: 12px;
            }
            QLineEdit, QDateEdit {
                font-size: 14px;
                padding: 8px 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background-color: #ffffff;
                min-height: 32px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #4a90e2;
                background-color: #f8fafc;
                box-shadow: 0 0 4px rgba(74, 144, 226, 0.3);
            }
        """)

        # === Header ===
        header = QLabel("Certificate of Analysis")
        header.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #1a3c6c;
            margin-bottom: 20px;
            text-align: center;
        """)
        self.coa_form_layout.addWidget(header)

        # === Section 1: General Info ===
        form_layout.addRow(QLabel("Customer:"), self.coa_customer_input)
        form_layout.addRow(QLabel("Color Code:"), self.color_code_input)
        form_layout.addRow(QLabel("Quantity Delivered:"), self.quantity_delivered_input)
        deliver_date_layout = QHBoxLayout()
        deliver_date_layout.addWidget(self.delivery_date_input)
        deliver_date_layout.addStretch()
        form_layout.addRow(QLabel("Delivery Date:"), deliver_date_layout)
        form_layout.addRow(QLabel("Lot Number:"), self.lot_number_input)
        production_date_layout = QHBoxLayout()
        production_date_layout.addWidget(self.production_date_input)
        production_date_layout.addStretch()
        form_layout.addRow(QLabel("Production Date:"), production_date_layout)

        receipt_row = QHBoxLayout()
        receipt_row.addWidget(self.delivery_receipt_input)
        receipt_row.addSpacing(10)  # Add 10px spacing before P.O Number
        receipt_row.addWidget(QLabel("P.O Number:"))
        receipt_row.addWidget(self.po_number_input)
        form_layout.addRow(QLabel("Delivery Receipt:"), receipt_row)

        # === Section 2: Summary of Analysis ===
        section2_header = QLabel("Summary of Analysis")
        section2_header.setProperty("class", "sub_title")
        soa_layout = QHBoxLayout()
        soa_layout.addStretch()
        soa_layout.addWidget(section2_header)
        soa_layout.addStretch()
        form_layout.addRow(soa_layout)

        self.summary_analysis_table.setColumnCount(2)
        self.summary_analysis_table.setRowCount(3)
        self.summary_analysis_table.setHorizontalHeaderLabels(["Standard", "Delivery"])
        self.summary_analysis_table.setVerticalHeaderLabels([
            "Color", "Light Fastness (1-8)", "Heat Stability (1-5)"
        ])
        self.summary_analysis_table.setMinimumWidth(600)
        self.summary_analysis_table.setMaximumWidth(800)
        self.summary_analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.summary_analysis_table.resizeRowsToContents()
        self.summary_analysis_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.summary_analysis_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.summary_analysis_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ececec;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
            QTableWidget::item:hover {
                background-color: #f0f4f8;
            }
            QHeaderView::section {
                font-size: 15px;
                font-weight: 600;
                padding: 10px;
                background-color: #f0f4f8;
                border: 1px solid #d1d5db;
                color: #1a3c6c;
            }
            QHeaderView::section:horizontal {
                border-bottom: 2px solid #4a90e2;
            }
            QTableCornerButton::section {
                background-color: #f0f4f8;
                border: 1px solid #d1d5db;
            }
        """)
        adjust_table_height(self)

        table_container = QHBoxLayout()
        table_container.addStretch()
        table_container.addWidget(self.summary_analysis_table)
        table_container.addStretch()
        form_layout.addRow(table_container)

        # === Buttons ===
        btn_add_row = QPushButton("Add Row")
        btn_add_row.clicked.connect(self.add_row_to_coa_summary_table)
        btn_delete_row = QPushButton("Delete Row")
        btn_delete_row.clicked.connect(self.delete_row_from_coa_summary_table)
        btn_delete_row.setProperty("class", "delete")

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                min-height: 36px;
            }
            QPushButton[class="delete"] {
                background-color: #e63946;
            }
            QPushButton:hover {
                background-color: #45a049;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton[class="delete"]:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QPushButton[class="delete"]:pressed {
                background-color: #b71c1c;
            }
            QPushButton:focus {
                outline: none;
                border: 2px solid #4a90e2;
            }
        """

        btn_add_row.setStyleSheet(button_style)
        btn_delete_row.setStyleSheet(button_style)
        self.btn_coa_submit.setStyleSheet(button_style)

        btn_add_table_row = QHBoxLayout()
        btn_add_table_row.addStretch()
        btn_add_table_row.addWidget(btn_add_row)
        btn_add_table_row.addSpacing(16)
        btn_add_table_row.addWidget(btn_delete_row)
        btn_add_table_row.addStretch()
        form_layout.addRow(btn_add_table_row)

        certified_row = QHBoxLayout()
        certified_row.addWidget(self.certified_by_input)
        certified_row.addSpacing(10)  # Add 10px spacing before Date
        certified_row.addWidget(QLabel("Date:"))
        certified_row.addWidget(self.creation_date_input)
        form_layout.addRow(QLabel("Certified by:"), certified_row)

        form_layout.addRow(QLabel("Storage:"), self.coa_storage_input)
        form_layout.addRow(QLabel("Shelf Life:"), self.coa_shelf_life_input)
        form_layout.addRow(QLabel("Suitability:"), self.suitability_input)

        submit_button_row = QHBoxLayout()
        submit_button_row.addStretch()
        submit_button_row.addWidget(self.btn_coa_submit)
        submit_button_row.addStretch()
        form_layout.addRow(submit_button_row)

        self.coa_form_layout.addWidget(form_widget)
    except Exception as e:
        print(str(e))


def adjust_table_height(self):
    self.summary_analysis_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    fixed_row_height = 44
    for i in range(self.summary_analysis_table.rowCount()):
        self.summary_analysis_table.setRowHeight(i, fixed_row_height)
    row_height_total = self.summary_analysis_table.rowCount() * fixed_row_height
    header_height = self.summary_analysis_table.horizontalHeader().height()
    frame = 2 * self.summary_analysis_table.frameWidth()

    self.summary_analysis_table.setFixedHeight(row_height_total + header_height + frame)


def clear_coa_form(self):
    try:
        """Clear all input fields and the summary table."""
        global current_coa_id
        current_coa_id = None
        self.coa_customer_input.clear()
        self.color_code_input.clear()
        self.lot_number_input.clear()
        self.po_number_input.clear()
        self.delivery_receipt_input.clear()
        self.quantity_delivered_input.clear()
        self.certified_by_input.clear()
        self.coa_storage_input.clear()
        self.coa_shelf_life_input.clear()
        self.suitability_input.clear()

        self.delivery_date_input.setDate(QDate.currentDate())
        self.production_date_input.setDate(QDate.currentDate())
        self.creation_date_input.setDate(QDate.currentDate())

        self.summary_analysis_table.clearContents()
        self.summary_analysis_table.setColumnCount(2)
        self.summary_analysis_table.setRowCount(3)
        self.summary_analysis_table.setHorizontalHeaderLabels(["Standard", "Delivery"])
        self.summary_analysis_table.setVerticalHeaderLabels([
            "Color", "Light Fastness (1-8)", "Heat Stability (1-5)"
        ])
        self.btn_coa_submit.setText("Submit")

    except Exception as e:
        print(str(e))

from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QSizePolicy, QHeaderView, QPushButton, QInputDialog, QTableWidgetItem, \
    QFormLayout, QTableWidget, QLineEdit, QAbstractItemView, QWidget

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
    form_widget = QWidget()
    form_layout = QFormLayout()
    form_widget.setLayout(form_layout)

    form_layout.setHorizontalSpacing(20)
    form_layout.setVerticalSpacing(12)
    form_layout.setContentsMargins(20, 20, 70, 20)

    form_widget.setStyleSheet("""
            QLabel {
                margin-left: 60px;
                font-size: 16px;
            }
            QLineEdit, QTextEdit, QDateEdit {
                font-size: 16px;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .sub_title {
                font-size: 20px;
                font-weight: semi-bold;
                margin-top: 12px;
                margin-bottom: 8px;
            }
            
        """)

    # === Header ===
    header = QLabel("Certificate of Analysis")
    header.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.coa_form_layout.addWidget(header)

    # === Section 1: General Info ===
    form_layout.addRow(QLabel("Customer:"), self.coa_customer_input)
    form_layout.addRow(QLabel("Color Code:"), self.color_code_input)
    form_layout.addRow(QLabel("Quantity Delivered:"), self.quantity_delivered_input)
    deliver_date_layout = QHBoxLayout()
    deliver_date_layout.addWidget(self.delivery_date_input)
    deliver_date_layout.addStretch()
    deliver_date_layout.addStretch()
    form_layout.addRow(QLabel("Delivery Date:"), deliver_date_layout)
    form_layout.addRow(QLabel("Lot Number:"), self.lot_number_input)
    production_date_layout = QHBoxLayout()
    production_date_layout.addWidget(self.production_date_input)
    production_date_layout.addStretch()
    production_date_layout.addStretch()
    form_layout.addRow(QLabel("Production Date:"), production_date_layout)

    receipt_row = QHBoxLayout()
    receipt_row.addWidget(self.delivery_receipt_input)
    receipt_row.addWidget(QLabel("P.O Number:"))
    receipt_row.addWidget(self.po_number_input)
    form_layout.addRow(QLabel("Delivery Receipt:"), receipt_row)


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
        "Color", "Light fastness (1-8)", "Heat Stability (1-5)"
    ])
    self.summary_analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.summary_analysis_table.resizeRowsToContents()
    self.summary_analysis_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.summary_analysis_table.setStyleSheet("""
        QTableWidget {
            font-size: 14px;  
        }
        QHeaderView::section:horizontal,
        QHeaderView::section:vertical{
            font-size: 16px;
            padding: 0 4px;
            font-weight: semi-bold;
            background-color: #f0f0f0;  
            border: 1px solid lightgray;
        }
        QTableCornerButton::section {
            background-color: #f0f0f0;
            border: 1px solid lightgray;
        }
    """)
    adjust_table_height(self)

    table_container = QHBoxLayout()
    table_container.addStretch()

    table_container.addWidget(self.summary_analysis_table)
    table_container.addStretch()

    self.coa_data_entry_tab.resizeEvent = lambda event: self.resize_summary_table()
    # Add to form layout
    form_layout.addRow(table_container)

    btn_add_row = QPushButton("Add Row")
    btn_add_row.clicked.connect(self.add_row_to_coa_summary_table)
    btn_delete_row = QPushButton("Delete Row")
    btn_delete_row.setProperty("class", "delete")

    button_style = """
        QPushButton {
            background-color: #4CAF50;  /* Green */
            color: white;
            font-size: 14px;
            font-weight: semi-bold;
            padding: 6px 14px;
            border: 1px solid #388E3C;
            border-radius: 6px;
            min-width: 80px;
        }
        QPushButton[class="delete"] {
            background-color: #E53935;  /* Red */
            border: 1px solid #C62828;
        }
        QPushButton:hover {
            background-color: #45A049;
        }
        QPushButton[class="delete"]:hover {
            background-color: #D32F2F;
        }
        QPushButton:pressed {
            background-color: #397D3A;
        }
        QPushButton[class="delete"]:pressed {
            background-color: #B71C1C;
        }
    """

    # Apply styles
    btn_add_row.setStyleSheet(button_style)
    btn_delete_row.setStyleSheet(button_style)
    self.btn_coa_submit.setStyleSheet(button_style)

    btn_add_table_row = QHBoxLayout()
    btn_add_table_row.addStretch()
    btn_add_table_row.addStretch()
    btn_add_table_row.addStretch()
    btn_add_table_row.addWidget(btn_add_row)
    btn_add_table_row.addStretch()
    btn_add_table_row.addWidget(btn_delete_row)
    btn_add_table_row.addStretch()
    btn_add_table_row.addStretch()
    btn_add_table_row.addStretch()
    form_layout.addRow(btn_add_table_row)

    certified_row = QHBoxLayout()
    certified_row.addWidget(self.certified_by_input)
    certified_row.addWidget(QLabel("Date:"))
    certified_row.addWidget(self.creation_date_input)
    form_layout.addRow(QLabel("Certified by:"), certified_row)

    form_layout.addRow(QLabel("Storage:"), self.coa_storage_input)
    form_layout.addRow(QLabel("Shelf Life:"), self.coa_shelf_life_input)
    form_layout.addRow(QLabel("Suitability:"), self.suitability_input)

    # === Submit button centered ===
    submit_button_row = QHBoxLayout()
    submit_button_row.addStretch()
    submit_button_row.addWidget(self.btn_coa_submit)
    submit_button_row.addStretch()
    form_layout.addRow(submit_button_row)

    self.coa_form_layout.addWidget(form_widget)


def adjust_table_height(self):
    self.summary_analysis_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    fixed_row_height = 40
    for i in range(self.summary_analysis_table.rowCount()):
        self.summary_analysis_table.setRowHeight(i, fixed_row_height)
    # Total height = all rows + horizontal header + frame
    row_height_total = self.summary_analysis_table.rowCount() * fixed_row_height
    header_height = self.summary_analysis_table.horizontalHeader().height()
    frame = 2 * self.summary_analysis_table.frameWidth()

    self.summary_analysis_table.setFixedHeight(row_height_total + header_height + frame)


def clear_coa_form(self):
    """Clear all input fields and the summary table."""
    # Clear QLineEdit/QTextEdit fields
    global current_coa_id
    current_coa_id = None  # Reset the global COA ID
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

    # Clear QDateEdit fields
    self.delivery_date_input.setDate(QDate.currentDate())
    self.production_date_input.setDate(QDate.currentDate())
    self.creation_date_input.setDate(QDate.currentDate())

    # Reset table
    self.summary_analysis_table.clearContents()
    self.summary_analysis_table.setColumnCount(2)
    self.summary_analysis_table.setRowCount(3)
    self.summary_analysis_table.setHorizontalHeaderLabels(["Standard", "Delivery"])
    self.summary_analysis_table.setVerticalHeaderLabels([
        "Color", "Light fastness (1-8)", "Heat Stability (1-5)"
    ])

    # Reset submit button
    self.btn_coa_submit.setText("Submit")


from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QSizePolicy, QHeaderView, QPushButton, QInputDialog, QTableWidgetItem, \
    QFormLayout, QTableWidget, QLineEdit, QAbstractItemView


def coa_data_entry_form(self):
    form_layout = QFormLayout()
    form_layout.setHorizontalSpacing(20)
    form_layout.setVerticalSpacing(12)
    form_layout.setContentsMargins(20, 20, 20, 20)

    header = QLabel("Certificate of Analysis")
    header.setStyleSheet("font-size: 18px; font-weight: bold; ")

    # === Table ===
    self.summary_analysis_table.setColumnCount(2)
    self.summary_analysis_table.setRowCount(3)
    self.summary_analysis_table.setHorizontalHeaderLabels(["Standard", "Delivery"])
    self.summary_analysis_table.setVerticalHeaderLabels([
        "Color", "Light fastness (1-8)", "Heat Stability (1-5)"
    ])
    self.summary_analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.summary_analysis_table.resizeRowsToContents()
    self.summary_analysis_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    adjust_table_height(self)

    # === Add Row Button ===
    btn_add_row = QPushButton("Add Row")
    btn_add_table_row = QHBoxLayout()
    btn_add_table_row.addStretch()
    btn_add_table_row.addWidget(btn_add_row)
    btn_add_table_row.addStretch()

    btn_add_row.clicked.connect(self.add_row_to_coa_summary_table)

    # === Add widgets to form layout ===
    form_layout.addRow(header)

    form_layout.addRow("Customer:", self.coa_customer_input)
    form_layout.addRow("Color Code:", self.color_code_input)
    form_layout.addRow("Quantity Delivered:", self.quantity_delivered_input)
    form_layout.addRow("Delivery Date:", self.delivery_date_input)
    form_layout.addRow("Lot Number:", self.lot_number_input)
    form_layout.addRow("Production Date:", self.production_date_input)

    # Row with multiple widgets
    receipt_row = QHBoxLayout()
    receipt_row.addWidget(self.delivery_receipt_input)
    receipt_row.addWidget(QLabel("P.O Number:"))
    receipt_row.addWidget(self.po_number_input)
    form_layout.addRow("Delivery Receipt:", receipt_row)

    # Table with header
    summary_header = QLabel("Summary of Analysis")
    summary_header.setStyleSheet("font-weight: bold; margin-top: 12px;")
    form_layout.addRow(summary_header)
    form_layout.addRow(self.summary_analysis_table)
    form_layout.addRow(btn_add_table_row)

    certified_row = QHBoxLayout()
    certified_row.addWidget(self.certified_by_input)
    certified_row.addWidget(QLabel("Date:"))
    certified_row.addWidget(self.creation_date_input)
    form_layout.addRow("Certified by:", certified_row)

    form_layout.addRow("Storage:", self.coa_storage_input)
    form_layout.addRow("Shelf Life:", self.coa_shelf_life_input)
    form_layout.addRow("Suitability:", self.suitability_input)

    # Centered submit button
    submit_button_row = QHBoxLayout()
    submit_button_row.addStretch()
    submit_button_row.addWidget(self.btn_coa_submit)
    submit_button_row.addStretch()
    form_layout.addRow(submit_button_row)

    self.coa_form_layout.addLayout(form_layout)


def adjust_table_height(self):
    """Resize table to fit rows dynamically."""
    row_height = sum([self.summary_analysis_table.rowHeight(i)
                      for i in range(self.summary_analysis_table.rowCount())])
    header_height = self.summary_analysis_table.horizontalHeader().height()
    self.summary_analysis_table.setFixedHeight(row_height + header_height + 2)



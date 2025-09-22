from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget

from db import db_con
from utils import abs_path


def load_msds_table(self):
    self.msds_records_table.setRowCount(0)

    records = db_con.get_all_msds_data()

    if not records:
        # Optional: Display a message or leave the table empty
        # For example, you could add a row with "No data available"
        self.msds_records_table.insertRow(0)
        no_data_item = self.create_readonly_item("No MSDS records found.", column_idx=0)
        self.msds_records_table.setItem(0, 0, no_data_item)
        # You might want to span this item across all columns
        self.msds_records_table.setSpan(0, 0, 1, self.msds_records_table.columnCount())
        return # Exit the function as there's no data to process

    for row_idx, record in enumerate(records):
        msds_id = record[0]
        customer_name = record[1]
        product_code = record[3]
        creation_date = record[4]
        revision_date_str = creation_date.strftime("%m-%d-%Y")

        display_text = f"{customer_name} {product_code} MSDS {revision_date_str}".upper()

        self.msds_records_table.insertRow(row_idx)
        self.msds_records_table.setItem(row_idx, 0, self.create_readonly_item(display_text, column_idx=0))

        # Column 1 → View icon
        view_item = self.create_readonly_item(icon_path=abs_path.resource("img/view_icon.png"), selectable=False)
        view_item.setToolTip("View")
        self.msds_records_table.setItem(row_idx, 1, view_item)

        # Column 2 → Edit icon
        edit_item = self.create_readonly_item(icon_path=abs_path.resource("img/edit_icon.png"), selectable=False)
        edit_item.setToolTip("Edit")
        self.msds_records_table.setItem(row_idx, 2, edit_item)

        # Column 3 → Delete icon
        delete_item = self.create_readonly_item(icon_path=abs_path.resource("img/delete_icon.png"), selectable=False)
        delete_item.setToolTip("Delete")
        self.msds_records_table.setItem(row_idx, 3, delete_item)

        # store msds_id as hidden data inside column 0
        self.msds_records_table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, msds_id)


def load_coa_table(self):
    self.coa_records_table.setRowCount(0)

    # Get data from DB
    records = db_con.get_all_coa_data()

    if not records:
        # Optional: Display a message or leave the table empty
        # For example, you could add a row with "No data available"
        self.coa_records_table.insertRow(0)
        no_data_item = self.create_readonly_item("No COA records found.", column_idx=0)
        self.coa_records_table.setItem(0, 0, no_data_item)
        # You might want to span this item across all columns
        self.coa_records_table.setSpan(0, 0, 1, self.coa_records_table.columnCount())
        return

    for row_idx, record in enumerate(records):
        # unpack fields from your table (adjust indexes if needed)
        coa_id = record[0]  # id is usually first
        customer_name = record[1]
        color_code = record[2]
        lot_number = record[3]
        delivery_receipt_number = record[5]
        delivery_date = record[7]
        delivery_date_str = delivery_date.strftime("%m%d%y")

        # build display text
        display_text = f"{delivery_date_str} DRN{delivery_receipt_number} COA {customer_name} {color_code} {lot_number}".upper()

        # insert row
        self.coa_records_table.insertRow(row_idx)
        self.coa_records_table.setItem(row_idx, 0, self.create_readonly_item(display_text, column_idx=0))

        # Column 1 → View icon
        view_item = self.create_readonly_item(icon_path=abs_path.resource("img/view_icon.png"), selectable=False)
        view_item.setToolTip("View")
        self.coa_records_table.setItem(row_idx, 1, view_item)

        # Column 2 → Edit icon
        edit_item = self.create_readonly_item(icon_path=abs_path.resource("img/edit_icon.png"), selectable=False)
        edit_item.setToolTip("Edit")
        self.coa_records_table.setItem(row_idx, 2, edit_item)

        # Column 3 → Delete icon
        delete_item = self.create_readonly_item(icon_path=abs_path.resource("img/delete_icon.png"), selectable=False)
        delete_item.setToolTip("Delete")
        self.coa_records_table.setItem(row_idx, 3, delete_item)

        # store coa_id as hidden data inside column 0
        self.coa_records_table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, coa_id)


def load_rrf_table(self):
    self.coa_records_table.setRowCount(0)

    # Get data from DB
    records = db_con.get_all_coa_data_rrf()

    if not records:
        # Optional: Display a message or leave the table empty
        # For example, you could add a row with "No data available"
        self.coa_records_table.insertRow(0)
        no_data_item = self.create_readonly_item("No COA-RRF records found.", column_idx=0)
        self.coa_records_table.setItem(0, 0, no_data_item)
        # You might want to span this item across all columns
        self.coa_records_table.setSpan(0, 0, 1, self.coa_records_table.columnCount())
        return

    for row_idx, record in enumerate(records):
        # unpack fields from your table (adjust indexes if needed)
        coa_id = record[0]  # id is usually first
        customer_name = record[1]
        color_code = record[2]
        lot_number = record[3]
        rrf_number = record[5]
        delivery_date = record[7]
        delivery_date_str = delivery_date.strftime("%m%d%y")

        # build display text
        display_text = f"{delivery_date_str} RRFN{rrf_number} COA {customer_name} {color_code} {lot_number}".upper()

        # insert row
        self.coa_records_table.insertRow(row_idx)
        self.coa_records_table.setItem(row_idx, 0, self.create_readonly_item(display_text, column_idx=0))

        # Column 1 → View icon
        view_item = self.create_readonly_item(icon_path=abs_path.resource("img/view_icon.png"), selectable=False)
        view_item.setToolTip("View")
        self.coa_records_table.setItem(row_idx, 1, view_item)

        # Column 2 → Edit icon
        edit_item = self.create_readonly_item(icon_path=abs_path.resource("img/edit_icon.png"), selectable=False)
        edit_item.setToolTip("Edit")
        self.coa_records_table.setItem(row_idx, 2, edit_item)

        # Column 3 → Delete icon
        delete_item = self.create_readonly_item(icon_path=abs_path.resource("img/delete_icon.png"), selectable=False)
        delete_item.setToolTip("Delete")
        self.coa_records_table.setItem(row_idx, 3, delete_item)

        # store coa_id as hidden data inside column 0
        self.coa_records_table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, coa_id)


def resize_columns(self, table: QTableWidget, event):
    total_width = table.viewport().width()
    icon_size = 30
    padding = 10
    icon_col_width = icon_size + padding

    # Set last 4 columns to icon width
    for col in range(1, table.columnCount()):
        table.setColumnWidth(col, icon_col_width)

    # First column = take the rest
    remaining_width = total_width - (icon_col_width * (table.columnCount() - 1))
    if remaining_width > 0:
        table.setColumnWidth(0, remaining_width)

    super(QTableWidget, table).resizeEvent(event)


def search_msds(self, query):
    query = query.strip().lower()
    for row in range(self.msds_records_table.rowCount()):
        item = self.msds_records_table.item(row, 0)  # column 0 has display_text
        if item:
            text = item.text().lower()
            match = query in text
            self.msds_records_table.setRowHidden(row, not match)


def search_coa(self, query):
    query = query.strip().lower()
    for row in range(self.coa_records_table.rowCount()):
        item = self.coa_records_table.item(row, 0)  # column 0 has display_text
        if item:
            text = item.text().lower()
            match = query in text
            self.coa_records_table.setRowHidden(row, not match)


def search_coa_rrf(self, query):
    query = query.strip().lower()
    for row in range(self.coa_records_table.rowCount()):
        item = self.coa_records_table.item(row, 0)  # column 0 has display_text
        if item:
            text = item.text().lower()
            match = query in text
            self.coa_records_table.setRowHidden(row, not match)


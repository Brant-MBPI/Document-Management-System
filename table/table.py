from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget

from db import db_con


def load_msds_table(self):
    self.msds_records_table.setRowCount(0)

    records = db_con.get_all_msds_data()
    for row_idx, record in enumerate(records):
        msds_id = record[0]
        creation_date = record[3]
        revision_date_str = creation_date.strftime("%m-%d-%Y")

        display_text = f"MSDS {revision_date_str}".upper()

        self.msds_records_table.insertRow(row_idx)
        self.msds_records_table.setItem(row_idx, 0, self.create_readonly_item(display_text, column_idx=0))
        self.msds_records_table.setItem(row_idx, 1,
                                        self.create_readonly_item(icon_path="img/view_icon.png", selectable=False))
        self.msds_records_table.setItem(row_idx, 2,
                                        self.create_readonly_item(icon_path="img/edit_icon.png", selectable=False))
        self.msds_records_table.setItem(row_idx, 3,
                                        self.create_readonly_item(icon_path="img/delete_icon.png", selectable=False))
        self.msds_records_table.setItem(row_idx, 4,
                                        self.create_readonly_item(icon_path="img/print_icon.png", selectable=False))

        # store msds_id as hidden data inside column 0
        self.msds_records_table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, msds_id)


def load_coa_table(self):
    self.coa_records_table.setRowCount(0)

    # Get data from DB
    records = db_con.get_all_coa_data()

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

        self.coa_records_table.setItem(row_idx, 1,
                                       self.create_readonly_item(icon_path="img/view_icon.png", selectable=False))
        self.coa_records_table.setItem(row_idx, 2,
                                       self.create_readonly_item(icon_path="img/edit_icon.png", selectable=False))
        self.coa_records_table.setItem(row_idx, 3,
                                       self.create_readonly_item(icon_path="img/delete_icon.png", selectable=False))
        self.coa_records_table.setItem(row_idx, 4,
                                       self.create_readonly_item(icon_path="img/print_icon.png", selectable=False))

        # store coa_id as hidden data inside column 0
        self.coa_records_table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, coa_id)


def resize_columns(self, table: QTableWidget, event):
    total_width = table.viewport().width()

    # Fixed size for icon columns (icon size + padding)
    icon_size = 24  # adjust this to your actual icon size
    padding = 10  # extra space so it's not cramped
    icon_col_width = icon_size + padding

    # Set last 4 columns to icon width
    for col in range(1, table.columnCount()):
        table.setColumnWidth(col, icon_col_width)

    # First column = take the rest
    remaining_width = total_width - (icon_col_width * (table.columnCount() - 1))
    if remaining_width > 0:
        table.setColumnWidth(0, remaining_width)

    super(QTableWidget, table).resizeEvent(event)

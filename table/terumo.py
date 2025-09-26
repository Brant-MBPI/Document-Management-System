import re

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QLabel, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QGroupBox, QGridLayout
)
from utils import abs_path

def coa_entry_form(self):
    try:
        form_widget = QWidget()
        main_v_layout = QVBoxLayout(form_widget)
        main_v_layout.setContentsMargins(30, 20, 30, 30)
        calendar_icon_path = abs_path.resource("img/calendar_icon.png").replace("\\", "/")

        form_widget.setStyleSheet(f"""
            QWidget {{
                background-color: #f8f9fa;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                color: #343a40;
            }}
            QLabel {{
                font-size: 14px;
                font-weight: 500;
                color: #495057;
                padding-bottom: 2px;
                background-color: transparent;
            }}
            QLabel[class="subsection_title"] {{
                font-size: 16px;
                font-weight: 600;
                color: #212529;
                margin-top: 10px;
                margin-bottom: 8px;
            }}
            QLineEdit, QDateEdit, QTextEdit {{
                font-size: 12px;
                padding: 6px 8px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: #ffffff;
                min-height: 28px;
                selection-background-color: #aed6f1;
            }}
            QLineEdit:focus, QDateEdit:focus, QTextEdit:focus {{
                border: 1px solid #007bff;
                background-color: #e9f5ff;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
            }}
            QDateEdit::drop-down {{
                border: 0px;
                width: 40px;
                background-color: #e9ecef;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            QDateEdit::down-arrow {{
                background-image: url("{calendar_icon_path}");
                width: 26px;
                height: 26px;
            }}
            QDateEdit::drop-down:hover {{
                background-color: #dee2e6;
            }}
            QDateEdit::down-arrow:on {{
                top: 1px;
                left: 1px;
            }}
            QGroupBox {{
                font-size: 14px;
                font-weight: 600;
                color: #212529;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 2.0ex;
                background-color: #ffffff;
                padding: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                left: 15px;
                margin-left: 0px;
                color: #34495e;
                background-color: #f8f9fa;
            }}
        """)

        # === Header ===
        header = QLabel("Certificate of Analysis - Terumo")
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid #007bff;
            text-align: center;
        """)
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(header)
        header_layout.addStretch()
        main_v_layout.addLayout(header_layout)

        # === General Info ===
        general_info_group = QGroupBox()
        general_info_layout = QGridLayout()
        general_info_group.setLayout(general_info_layout)

        general_info_layout.setHorizontalSpacing(30)
        general_info_layout.setVerticalSpacing(15)
        general_info_layout.setContentsMargins(20, 25, 20, 20)

        # Rearranged to closer match PDF order
        general_info_layout.addWidget(QLabel("Customer:"), 0, 0, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_customer_input, 0, 1)
        general_info_layout.addWidget(QLabel("Delivery Date:"), 0, 2, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_delivery_date, 0, 3)

        general_info_layout.addWidget(QLabel("Item Code:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_item_code, 1, 1)
        general_info_layout.addWidget(QLabel("Item Description:"), 1, 2, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_item_description, 1, 3)

        general_info_layout.addWidget(QLabel("Lot No.:"), 2, 0, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_lot_number, 2, 1)
        general_info_layout.addWidget(QLabel("Quantity:"), 2, 2, Qt.AlignmentFlag.AlignRight)
        general_info_layout.addWidget(self.terumo_quantity, 2, 3)

        main_v_layout.addWidget(general_info_group)

        # === Molded Chip Inspection ===
        molded_group = QGroupBox("Molded Chip Inspection")
        molded_layout = QVBoxLayout()
        molded_group.setLayout(molded_layout)
        molded_layout.setContentsMargins(20, 25, 20, 20)
        molded_layout.setSpacing(15)

        # Color subsection
        color_title = QLabel("Color")
        color_title.setProperty("class", "subsection_title")
        molded_layout.addWidget(color_title)

        color_grid = QGridLayout()
        color_grid.setHorizontalSpacing(30)
        color_grid.setVerticalSpacing(10)
        color_grid.addWidget(QLabel("Standard:"), 0, 0, Qt.AlignmentFlag.AlignRight)
        color_grid.addWidget(self.terumo_color_std, 0, 1)
        color_grid.addWidget(QLabel("Actual:"), 0, 2, Qt.AlignmentFlag.AlignRight)
        color_grid.addWidget(self.terumo_color_actual, 0, 3)
        color_grid.addWidget(QLabel("Judgement:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        color_grid.addWidget(self.terumo_color_judgement, 1, 1)
        molded_layout.addLayout(color_grid)

        # Foreign Material Contamination subsection
        foreign_title = QLabel("Foreign Material Contamination")
        foreign_title.setProperty("class", "subsection_title")
        molded_layout.addWidget(foreign_title)

        foreign_grid = QGridLayout()
        foreign_grid.setHorizontalSpacing(30)
        foreign_grid.setVerticalSpacing(10)

        # Headers for columns
        foreign_grid.addWidget(QLabel(""), 0, 0, Qt.AlignmentFlag.AlignLeft)
        foreign_grid.addWidget(QLabel("Diameter (mm):"), 0, 1, Qt.AlignmentFlag.AlignLeft)
        foreign_grid.addWidget(QLabel("Area (mm²):"), 0, 2, Qt.AlignmentFlag.AlignLeft)
        foreign_grid.addWidget(QLabel("Count:"), 0, 3, Qt.AlignmentFlag.AlignLeft)
        foreign_grid.addWidget(QLabel("Actual:"), 0, 4, Qt.AlignmentFlag.AlignLeft)

        # Row 1
        foreign_grid.addWidget(QLabel(""), 1, 0)
        foreign_grid.addWidget(self.terumo_foreign_diameter1, 1, 1)
        foreign_grid.addWidget(self.terumo_foreign_area1, 1, 2)
        foreign_grid.addWidget(self.terumo_foreign_count1, 1, 3)
        foreign_grid.addWidget(self.terumo_foreign_actual1, 1, 4)

        # Row 2
        foreign_grid.addWidget(QLabel(""), 2, 0)
        foreign_grid.addWidget(self.terumo_foreign_diameter2, 2, 1)
        foreign_grid.addWidget(self.terumo_foreign_area2, 2, 2)
        foreign_grid.addWidget(self.terumo_foreign_count2, 2, 3)
        foreign_grid.addWidget(self.terumo_foreign_actual2, 2, 4)

        foreign_grid.addWidget(QLabel("Judgement:"), 3, 0, Qt.AlignmentFlag.AlignLeft)
        foreign_grid.addWidget(self.terumo_foreign_judgement, 3, 1, 1, 2)

        molded_layout.addLayout(foreign_grid)

        main_v_layout.addWidget(molded_group)

        # === Pellet Inspection ===
        pellet_group = QGroupBox("Pellet Inspection")
        pellet_layout = QVBoxLayout()
        pellet_group.setLayout(pellet_layout)
        pellet_layout.setContentsMargins(20, 25, 20, 20)
        pellet_layout.setSpacing(15)

        # Appearance subsection
        appearance_title = QLabel("Appearance")
        appearance_title.setProperty("class", "subsection_title")
        pellet_layout.addWidget(appearance_title)

        appearance_grid = QGridLayout()
        appearance_grid.setHorizontalSpacing(30)
        appearance_grid.setVerticalSpacing(10)
        appearance_grid.addWidget(QLabel("Standard:"), 0, 0, Qt.AlignmentFlag.AlignRight)
        appearance_grid.addWidget(self.terumo_appearance_std, 0, 1, 1, 5)  # Span across
        appearance_grid.addWidget(QLabel("Start:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        appearance_grid.addWidget(self.terumo_appearance_start, 1, 1)
        appearance_grid.addWidget(QLabel("Middle:"), 1, 2, Qt.AlignmentFlag.AlignRight)
        appearance_grid.addWidget(self.terumo_appearance_mid, 1, 3)
        appearance_grid.addWidget(QLabel("End:"), 1, 4, Qt.AlignmentFlag.AlignRight)
        appearance_grid.addWidget(self.terumo_appearance_end, 1, 5)
        appearance_grid.addWidget(QLabel("Judgement:"), 2, 0, Qt.AlignmentFlag.AlignRight)
        appearance_grid.addWidget(self.terumo_appearance_judgement, 2, 1, 1, 2)
        pellet_layout.addLayout(appearance_grid)

        # Dimension subsection
        dimension_title = QLabel("Dimension")
        dimension_title.setProperty("class", "subsection_title")
        pellet_layout.addWidget(dimension_title)

        dimension_grid = QGridLayout()
        dimension_grid.setHorizontalSpacing(30)
        dimension_grid.setVerticalSpacing(10)
        dimension_grid.addWidget(QLabel("Standard:"), 0, 0, Qt.AlignmentFlag.AlignRight)
        dimension_grid.addWidget(self.terumo_dimension_std, 0, 1, 1, 5)  # Span across
        dimension_grid.addWidget(QLabel("Start:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        dimension_grid.addWidget(self.terumo_dimension_start, 1, 1)
        dimension_grid.addWidget(QLabel("Middle:"), 1, 2, Qt.AlignmentFlag.AlignRight)
        dimension_grid.addWidget(self.terumo_dimension_middle, 1, 3)
        dimension_grid.addWidget(QLabel("End:"), 1, 4, Qt.AlignmentFlag.AlignRight)
        dimension_grid.addWidget(self.terumo_dimension_end, 1, 5)
        dimension_grid.addWidget(QLabel("Judgement:"), 2, 0, Qt.AlignmentFlag.AlignRight)
        dimension_grid.addWidget(self.terumo_dimension_judgement, 2, 1, 1, 2)
        pellet_layout.addLayout(dimension_grid)

        main_v_layout.addWidget(pellet_group)

        # === Remarks & Approved By ===
        remarks_group = QGroupBox("Remarks & Approval")
        remarks_layout = QGridLayout()
        remarks_group.setLayout(remarks_layout)
        remarks_layout.setHorizontalSpacing(30)
        remarks_layout.setVerticalSpacing(15)
        remarks_layout.setContentsMargins(20, 25, 20, 20)

        remarks_layout.addWidget(QLabel("Remarks:"), 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        remarks_layout.addWidget(self.terumo_remarks, 0, 1, 1, 2)
        remarks_layout.addWidget(QLabel(""), 1, 1, 1, 3)
        self.terumo_remarks.setMinimumHeight(100)
        remarks_layout.addWidget(QLabel("Approved By:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        remarks_layout.addWidget(self.terumo_approved_by, 1, 1, 1, 2)
        remarks_layout.addWidget(QLabel(""), 1, 1, 1, 3)

        main_v_layout.addWidget(remarks_group)

        # === Submit Button ===
        submit_button_style = """
            QPushButton {
                background-color: #007bff;
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
                min-width: 120px;
                min-height: 40px;
                transition: background-color 0.2s ease, box-shadow 0.2s ease;
            }
            QPushButton:hover {
                background-color: #0056b3;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:focus {
                outline: none;
                border: 2px solid #007bff;
            }
        """
        self.terumo_submit_btn.setStyleSheet(submit_button_style)

        submit_button_row = QHBoxLayout()
        submit_button_row.addStretch()
        submit_button_row.addWidget(self.terumo_submit_btn)
        submit_button_row.addStretch()
        main_v_layout.addLayout(submit_button_row)

        main_v_layout.addStretch(1)

        self.terumo_form_layout.addWidget(form_widget)
    except Exception as e:
        print(f"Error loading Terumo COA form: {e}")
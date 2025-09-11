import sys
import traceback

from PyQt6.QtCore import Qt, QDate, QRegularExpression, QTimer, QEvent, QObject
from PyQt6.QtGui import QIcon, QIntValidator, QRegularExpressionValidator, QFont, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem, QScrollArea, QTextEdit, QPushButton, QDateEdit, \
    QInputDialog, QMessageBox, QAbstractItemView
from db import db_con
from alert import window_alert
from table import msds_data_entry, coa_data_entry, table
from print.print_msds import FileMSDS
from print.print_coa import FileCOA


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_tabs = QTabWidget()

        self.msds_form_layout = QVBoxLayout()
        self.msds_btn_layout = QHBoxLayout()
        self.coa_btn_layout = QHBoxLayout()
        self.coa_form_layout = QVBoxLayout()

        # MSDS FORM init
            #Section 1
        self.trade_label_input = QLineEdit()
        self.manufactured_label_input = QTextEdit()
        self.manufactured_label_input.setTabChangesFocus(True)
        self.tel_label_input = QLineEdit()
        tel_regex = QRegularExpression(r'^(\d{7,12}|\(\d{1,4}\)\s?\d{6,10})$')
        tel_validator = QRegularExpressionValidator(tel_regex)
        self.tel_label_input.setValidator(tel_validator)
        self.tel_label_timer = self.setup_finished_typing(
            self.tel_label_input, self.check_tel_number, delay=3000
        )

        self.facsimile_label_input = QLineEdit()
        self.facsimile_label_input.setValidator(tel_validator)
        self.facsimile_label_timer = self.setup_finished_typing(
            self.facsimile_label_input, self.check_tel_number, delay=3000
        )
        self.email_label_input = QLineEdit()
        email_regex = QRegularExpression(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')
        email_validator = QRegularExpressionValidator(email_regex)
        self.email_label_input.setValidator(email_validator)
        self.email_label_timer = self.setup_finished_typing(
            self.email_label_input, self.check_email, delay=3000
        )

            #Section2
        self.composition_input = QTextEdit()
        self.composition_input.setTabChangesFocus(True)
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
        self.fire_fighting_media_input.setTabChangesFocus(True)
            #Section6
        self.accidental_release_input = QTextEdit()
        self.accidental_release_input.setTabChangesFocus(True)
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
        heat_regex = QRegularExpression(r'^[1-5](-[1-5])?$')
        heat_validator = QRegularExpressionValidator(heat_regex)
        self.heat_stability_input = QLineEdit()
        self.heat_stability_input.setValidator(heat_validator)
        light_regex = QRegularExpression(r'^[1-8](-[1-8])?$')
        light_validator = QRegularExpressionValidator(light_regex)
        self.light_fastness_input = QLineEdit()
        self.light_fastness_input.setValidator(light_validator)
        self.decomposition_input = QLineEdit()
        self.flash_point_input = QLineEdit()
        self.auto_ignition_input = QLineEdit()
        self.explosion_property_input = QLineEdit()
        self.solubility_input = QLineEdit()
            #Section10
        self.stability_reactivity_input = QTextEdit()
        self.stability_reactivity_input.setTabChangesFocus(True)
            #Section11
        self.toxicological_input = QTextEdit()
        self.toxicological_input.setTabChangesFocus(True)
            #Section12
        self.ecological_input = QTextEdit()
        self.ecological_input.setTabChangesFocus(True)
            #Section13
        self.disposal_input = QTextEdit()
        self.disposal_input.setTabChangesFocus(True)
            #Section14
        self.transport_input = QTextEdit()
        self.transport_input.setTabChangesFocus(True)
            #Section15
        self.regulatory_input = QTextEdit()
        self.regulatory_input.setTabChangesFocus(True)
            #Section16
        self.msds_shelf_life_input = QTextEdit()
        self.msds_shelf_life_input.setTabChangesFocus(True)
            #Section17
        self.other_input = QTextEdit()
        self.other_input.setTabChangesFocus(True)
            #Submit Button
        self.btn_msds_submit = QPushButton("Submit")
        self.btn_msds_submit.setProperty("class", "msds_submit_btn")
        self.btn_msds_submit.clicked.connect(self.msds_btn_submit_clicked)

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
        self.btn_coa_submit = QPushButton("Submit")
        self.btn_coa_submit.clicked.connect(self.coa_btn_submit_clicked)

        self.po_number_input.setValidator((QIntValidator(0, 2147483647)))
        self.quantity_delivered_input.setValidator((QIntValidator(0, 2147483647)))

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
        self.msds_tab.setObjectName("msds_tab")
        self.coa_tab.setObjectName("coa_tab")

        self.msds_search_bar = QLineEdit()
        self.msds_search_bar.setPlaceholderText("Search...")
        search_icon_msds = QAction(QIcon("img/search_icon.png"), "Search", self.msds_search_bar)
        self.msds_search_bar.addAction(search_icon_msds, QLineEdit.ActionPosition.TrailingPosition)
        self.coa_search_bar = QLineEdit()
        self.coa_search_bar.setPlaceholderText("Search...")
        search_icon_coa = QAction(QIcon("img/search_icon.png"), "Search", self.coa_search_bar)
        self.coa_search_bar.addAction(search_icon_coa, QLineEdit.ActionPosition.TrailingPosition)

        self.msds_sub_tabs.setCornerWidget(self.msds_search_bar)
        self.coa_sub_tabs.setCornerWidget(self.coa_search_bar)

        self.msds_sub_tabs.currentChanged.connect(self.toggle_msds_search_bar)
        self.coa_sub_tabs.currentChanged.connect(self.toggle_coa_search_bar)

        self.msds_records_table = QTableWidget()
        self.msds_records_table.setProperty("class", "records_table")

        self.msds_records_layout = QVBoxLayout(self.msds_records_tab)  # inside MSDS sub-tab Records
        self.msds_records_layout.addWidget(self.msds_records_table)

        msds_scroll_area = QScrollArea(self.msds_data_entry_tab)
        msds_scroll_area.setWidgetResizable(True)

        # Form container inside the scroll area
        msds_form_container = QWidget()
        msds_form_layout = QVBoxLayout(msds_form_container)

        msds_form_layout.addLayout(self.msds_form_layout)
        msds_form_layout.addLayout(self.msds_btn_layout)

        msds_scroll_area.setWidget(msds_form_container)

        # Final layout for the tab
        self.msds_data_entry_layout = QVBoxLayout(self.msds_data_entry_tab)
        self.msds_data_entry_layout.addWidget(msds_scroll_area)

        # === COA Scroll Area ===
        coa_scroll_area = QScrollArea(self.coa_data_entry_tab)
        coa_scroll_area.setWidgetResizable(True)

        # Form container inside the scroll area
        coa_form_container = QWidget()
        coa_form_layout = QVBoxLayout(coa_form_container)

        coa_form_layout.addLayout(self.coa_form_layout)
        coa_form_layout.addLayout(self.coa_btn_layout)

        coa_scroll_area.setWidget(coa_form_container)

        self.coa_data_entry_layout = QVBoxLayout(self.coa_data_entry_tab)
        self.coa_data_entry_layout.addWidget(coa_scroll_area)

        #Inside COA Records Tab
        self.coa_records_table = QTableWidget()
        self.coa_records_table.setProperty("class", "records_table")

        self.coa_records_layout = QVBoxLayout(self.coa_records_tab)  # inside COA sub-tab Records
        self.coa_records_layout.addWidget(self.coa_records_table)

        self.coa_data_entry_layout = QVBoxLayout(self.coa_data_entry_tab)  # inside COA sub-tab Data Entry
        self.coa_data_entry_layout.addLayout(self.coa_form_layout)

        self.main_layout.addWidget(self.main_tabs)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        search_style = """
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 4px 20px 6px 10px;
                background-color: #f9f9f9;
                font-size: 12px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
                background-color: #ffffff;
            }
        """
        self.setStyleSheet("""
            QTableWidget[class="records_table"] {
                font-size: 15px;  /* Larger cell font */
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;  /* Rounded corners */
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow */
            }
            QTableWidget[class="records_table"]::item {
                padding: 12px;  /* Increased padding */
                border-bottom: 1px solid #e0e0e0;
                background-color: #ffffff;
            }
            QTableWidget[class="records_table"]::item:alternate {
                background-color: #f9fafb;  /* Alternating row color */
            }
            QTableWidget[class="records_table"]::item:selected {
                background-color: #e3f2fd;  /* Match coa_data_entry selection */
                color: #000000;
                border: 2px solid #0078d7;
            }
            QTableWidget[class="records_table"]::item:hover {
                background-color: #e9f3ff;  /* Match coa_data_entry hover */
            }
            QTableWidget[class="records_table"] QHeaderView::section {
                font-size: 16px;  /* Larger header font */
                font-weight: 600;
                padding: 12px;
                background-color: #f0f4f8;  /* Slightly lighter header */
                border: 1px solid #d1d5db;
                color: #1a3c6c;
            }
            QTableWidget[class="records_table"] QHeaderView::section:horizontal {
                border-right: none;
                border-bottom: 3px solid #4a90e2;  /* Blue underline */
            }
            QTableCornerButton::section {
                background-color: #f0f4f8;
                border: 1px solid #d1d5db;
            }
            QPushButton[class="msds_submit_btn"] {
                background-color: #4CAF50;
                color: white;
                padding: 12px 26px;
                margin: 0 70px 20px 0;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton[class="msds_submit_btn"]:hover {
                background-color: #45a049;
            }
            QPushButton[class="msds_submit_btn"]:pressed {
                background-color: #3e8e41;
            }
            QWidget#msds_tab, QWidget#coa_tab, QTabWidget {
                background-color: #f2f2f2;
                border: none;
            }
        """)
        tab_menu_style = """
            QTabWidget::pane {
                border: 1px solid #0066cc;
                border-radius: 6px;
                background-color: #f0f0f0;
                top: -1px;
            }
            QTabBar::tab {
                background: #f5f5f5;
                color: #333;
                padding: 8px 12px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-bottom: 1px solid #0066cc;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
                margin-top: 2px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #0078d7;
                font-weight: bold;
                border: 1px solid #0078d7;
                border-bottom: none;
                margin-top: 0px;
            }
            QTabBar::tab:hover {
                background: #e9f3ff;
                color: #005a9e;
            }
        """
        main_tab_style = """
            QTabBar::tab {
                background: #fafafa;
                color: #444;
                padding: 7px 16px;
                font-size: 14px;
                border: 1px solid #bbb;
                border-radius: 4px 4px 0 0;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #0066cc;
                font-weight: bold;
                border: 1px solid #0066cc;
            }
            QTabBar::tab:hover {
                background: #f0f7ff;
                color: #004a99;
            }
        """

        self.main_tabs.tabBar().setStyleSheet(main_tab_style)
        self.msds_sub_tabs.setStyleSheet(tab_menu_style)
        self.coa_sub_tabs.setStyleSheet(tab_menu_style)
        self.msds_search_bar.setStyleSheet(search_style)
        self.coa_search_bar.setStyleSheet(search_style)

        self.last_hovered = None
        self.msds_table_records_init()
        self.coa_table_records_init()
        # connect hover and clicked functions on table
        self.msds_records_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.msds_records_table.setMouseTracking(True)
        self.msds_records_table.cellEntered.connect(self.on_cell_hover)
        self.msds_records_table.cellClicked.connect(self.msds_cell_clicked)
        # connect search function
        self.msds_label_timer = self.setup_finished_typing(
            self.msds_search_bar,
            lambda: table.search_msds(self, self.msds_search_bar.text()),
            delay=600
        )
        self.coa_records_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.coa_records_table.setMouseTracking(True)
        self.coa_records_table.cellEntered.connect(self.on_cell_hover)
        self.coa_records_table.cellClicked.connect(self.coa_cell_clicked)
        self.coa_label_timer = self.setup_finished_typing(
            self.coa_search_bar,
            lambda: table.search_coa(self, self.coa_search_bar.text()),
            delay=600
        )
        table.load_msds_table(self)
        table.load_coa_table(self)
        coa_data_entry.coa_data_entry_form(self)

        msds_data_entry.create_form(self)

    def msds_btn_submit_clicked(self):
        try:
            # Collect all required fields
            required_fields = {
                "Trade Name": self.trade_label_input.text(),
                "Manufactured By": self.manufactured_label_input.toPlainText(),
                "Telephone No.": self.tel_label_input.text(),
                "Facsimile": self.facsimile_label_input.text(),
                "Email Adress": self.email_label_input.text(),
                "Composition/Information on Ingredients": self.composition_input.toPlainText(),
                "Hazard Preliminaries": self.hazard_preliminaries_input.text(),
                "Preliminary": self.hazard_entry_route_input.text(),
                "Symptoms of Exposure": self.hazard_symptoms_input.text(),
                "Restrictive Condition": self.hazard_restrictive_condition_input.text(),
                "Hazard Eyes": self.hazard_eyes_input.text(),
                "Hazard General Note": self.hazard_general_note_input.text(),
                "First Aid Inhalation": self.first_aid_inhalation_input.text(),
                "First Aid Eyes": self.first_aid_eyes.text(),
                "First Aid Skin": self.first_aid_skin_input.text(),
                "First Aid Ingestion": self.first_aid_ingestion_input.text(),
                "Extinguishing Media": self.fire_fighting_media_input.toPlainText(),
                "Accidental Release": self.accidental_release_input.toPlainText(),
                "Handling": self.handling_input.text(),
                "Storage": self.msds_storage_input.text(),
                "Exposure Control": self.exposure_control_input.text(),
                "Respiratory Protection": self.respiratory_protection_input.text(),
                "Hand Protection": self.hand_protection_input.text(),
                "Eye Protection": self.eye_protection_input.text(),
                "Skin Protection": self.skin_protection_input.text(),
                "Appearance": self.appearance_input.text(),
                "Odor": self.odor_input.text(),
                "Heat Stability": self.heat_stability_input.text(),
                "Light Fastness": self.light_fastness_input.text(),
                "Decomposition": self.decomposition_input.text(),
                "Flash Point": self.flash_point_input.text(),
                "Auto Ignition": self.auto_ignition_input.text(),
                "Explosion Property": self.explosion_property_input.text(),
                "Solubility": self.solubility_input.text(),
                "Stability & Reactivity": self.stability_reactivity_input.toPlainText(),
                "Toxicological": self.toxicological_input.toPlainText(),
                "Ecological": self.ecological_input.toPlainText(),
                "Disposal": self.disposal_input.toPlainText(),
                "Transport Information": self.transport_input.toPlainText(),
                "Regulatory": self.regulatory_input.toPlainText(),
                "Shelf Life": self.msds_shelf_life_input.toPlainText(),
                "Other": self.other_input.toPlainText()
            }

            # Check for empty values
            for field, value in required_fields.items():
                if not value.strip():  # empty string
                    window_alert.show_message(self, "Missing Input", f"Please fill in:   {field}", icon_type="warning")
                    return  # stop submission
            # If all fields are filled, proceed to save
            msds_data = {
                "trade_name": self.trade_label_input.text(),
                "manufacturer_info": self.manufactured_label_input.toPlainText(),
                "contact_tel": self.tel_label_input.text(),
                "contact_facsimile": self.facsimile_label_input.text(),
                "contact_email": self.email_label_input.text(),

                "composition_info": self.composition_input.toPlainText(),

                "hazard_preliminaries": self.hazard_preliminaries_input.text(),
                "hazard_entry_route": self.hazard_entry_route_input.text(),
                "hazard_symptoms": self.hazard_symptoms_input.text(),
                "hazard_restrictive_conditions": self.hazard_restrictive_condition_input.text(),
                "hazard_eyes": self.hazard_eyes_input.text(),
                "hazard_general_note": self.hazard_general_note_input.text(),

                "first_aid_inhalation": self.first_aid_inhalation_input.text(),
                "first_aid_eyes": self.first_aid_eyes.text(),
                "first_aid_skin": self.first_aid_skin_input.text(),
                "first_aid_ingestion": self.first_aid_ingestion_input.text(),

                "fire_fighting_media": self.fire_fighting_media_input.toPlainText(),
                "accidental_release_info": self.accidental_release_input.toPlainText(),
                "handling_info": self.handling_input.text(),
                "storage_info": self.msds_storage_input.text(),

                "exposure_control_info": self.exposure_control_input.text(),
                "respiratory_protection": self.respiratory_protection_input.text(),
                "hand_protection": self.hand_protection_input.text(),
                "eye_protection": self.eye_protection_input.text(),
                "skin_protection": self.skin_protection_input.text(),

                "appearance": self.appearance_input.text(),
                "odor": self.odor_input.text(),
                "heat_stability": self.heat_stability_input.text(),
                "light_fastness": self.light_fastness_input.text(),
                "decomposition_temp": self.decomposition_input.text(),
                "flash_point": self.flash_point_input.text(),
                "auto_ignition_temp": self.auto_ignition_input.text(),
                "explosion_property": self.explosion_property_input.text(),
                "solubility_water": self.solubility_input.text(),

                "stability_reactivity": self.stability_reactivity_input.toPlainText(),
                "toxicological_info": self.toxicological_input.toPlainText(),
                "ecological_info": self.ecological_input.toPlainText(),
                "disposal_info": self.disposal_input.toPlainText(),
                "transport_info": self.transport_input.toPlainText(),
                "regulatory_info": self.regulatory_input.toPlainText(),
                "shelf_life_info": self.msds_shelf_life_input.toPlainText(),
                "other_info": self.other_input.toPlainText()
            }

            # Save
            try:
                if msds_data_entry.current_msds_id is not None:  # Update existing MSDS
                    db_con.update_msds_sheet(msds_data_entry.current_msds_id, msds_data)
                    window_alert.show_message(self, "Success", "MSDS updated successfully!", icon_type="info")
                    msds_data_entry.current_msds_id = None
                else:  # Save new MSDS
                    db_con.save_msds_sheet(msds_data)
                    window_alert.show_message(self, "Success", "MSDS saved successfully!", icon_type="info")
            except Exception as e:
                window_alert.show_message(self, "Database Error", str(e), icon_type="critical")
            finally:
                msds_data_entry.clear_msds_form(self)
                table.load_msds_table(self)
        except Exception as e:
            window_alert.show_message(self, "Unexpected Error", f"An error occurred: {str(e)}", icon_type="critical")

    def coa_btn_submit_clicked(self):
        customer_name = self.coa_customer_input.text()
        color_code = self.color_code_input.text()
        quantity_delivered = self.quantity_delivered_input.text()
        delivery_date = self.delivery_date_input.date().toString("yyyy-MM-dd")
        lot_number = self.lot_number_input.text()
        production_date = self.production_date_input.date().toString("yyyy-MM-dd")
        delivery_receipt = self.delivery_receipt_input.text()
        po_number = self.po_number_input.text()
        summary_of_analysis = self.get_coa_summary_analysis_table_data()
        certified_by = self.certified_by_input.text()
        creation_date = self.creation_date_input.date().toString("yyyy-MM-dd")
        storage = self.coa_storage_input.text()
        shelf_life = self.coa_shelf_life_input.text()
        suitability = self.suitability_input.text()

        required_fields = {
            "Customer Name": customer_name,
            "Color Code": color_code,
            "Quantity Delivered": quantity_delivered,
            "Lot Number": lot_number,
            "Delivery Receipt": delivery_receipt,
            "PO Number": po_number,
            "Certified By": certified_by,
            "Storage": storage,
            "Shelf Life": shelf_life,
            "Suitability": suitability
        }

        # Check if any required field is empty
        for field, value in required_fields.items():
            if not value:  # empty string
                window_alert.show_message(self, "Missing Input", f"Please fill in:  {field}", icon_type="warning")
                return  # stop processing

        # Check summary of analysis if no empty row
        if not any(any(cell for cell in row) for row in summary_of_analysis.values()):
            window_alert.show_message(self, "Missing Input", "Please fill in the Summary of Analysis table.", icon_type="warning")
            return

        # Build coa_data for saving
        coa_data = {
            "customer_name": customer_name,
            "color_code": color_code,
            "lot_number": lot_number,
            "po_number": po_number,
            "delivery_receipt": delivery_receipt,
            "quantity_delivered": quantity_delivered,
            "delivery_date": delivery_date,
            "production_date": production_date,
            "creation_date": creation_date,
            "certified_by": certified_by,
            "storage": storage,
            "shelf_life": shelf_life,
            "suitability": suitability
        }

        # Save
        try:
            if coa_data_entry.current_coa_id is not None:  # Update existing COA
                db_con.update_certificate_of_analysis(coa_data_entry.current_coa_id, coa_data, summary_of_analysis)
                window_alert.show_message(self, "Success", f"Certificate of Analysis updated successfully!", icon_type="info")
                coa_data_entry.current_coa_id = None

            else:  # Save new COA
                db_con.save_certificate_of_analysis(coa_data, summary_of_analysis)
                window_alert.show_message(self,"Success", f"Certificate of Analysis saved successfully!", icon_type="info")
        except Exception as e:
            window_alert.show_message(self, "Database Error", str(e), icon_type="critical")
        finally:
            coa_data_entry.clear_coa_form(self)
            table.load_coa_table(self)
            coa_data_entry.adjust_table_height(self)

    def get_coa_summary_analysis_table_data(self):
        data = {}
        row_count = self.summary_analysis_table.rowCount()
        col_count = self.summary_analysis_table.columnCount()

        for row in range(row_count):
            # Get row header (vertical header text)
            header_item = self.summary_analysis_table.verticalHeaderItem(row)
            row_header = header_item.text() if header_item else f"Row {row}"

            # Get values in that row
            row_values = []
            for col in range(col_count):
                cell_item = self.summary_analysis_table.item(row, col)
                value = cell_item.text() if cell_item else ""
                row_values.append(value)

            # Store row header with its values
            data[row_header] = row_values

        return data

    def add_row_to_coa_summary_table(self):
        row_count = self.summary_analysis_table.rowCount()

        # Use the styled input function
        header_text, ok = window_alert.show_text_input(self, "New Row", "Enter row header:")

        if ok and header_text.strip():
            self.summary_analysis_table.insertRow(row_count)

            # Update headers
            current_headers = [self.summary_analysis_table.verticalHeaderItem(i).text()
                               for i in range(row_count)]
            current_headers.append(header_text.strip())
            self.summary_analysis_table.setVerticalHeaderLabels(current_headers)

            # Adjust table height
            coa_data_entry.adjust_table_height(self)

    def delete_row_from_coa_summary_table(self):
        selected_indexes = self.summary_analysis_table.selectionModel().selectedRows()

        if not selected_indexes:
            # No row selected, show a warning
            print(selected_indexes)
            window_alert.show_message(self, "Warning", "Please select a row to delete.", icon_type="warning")
            return

        row_to_delete = selected_indexes[0].row()  # Single selection, take the first

        # Show confirmation message
        confirm = window_alert.show_message(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete row {row_to_delete + 1}?",
            icon_type="question",
            is_confirmation=True
        )

        if confirm:
            self.summary_analysis_table.removeRow(row_to_delete)
            coa_data_entry.adjust_table_height(self)

    def create_readonly_item(self, text=None, icon_path=None, selectable=True, column_idx=None):
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

        if column_idx == 0:
            font = QFont()
            font.setPointSize(11)
            item.setFont(font)
        return item

    def msds_table_records_init(self):
        self.msds_records_table.setColumnCount(4)
        self.msds_records_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.msds_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.msds_records_table.horizontalHeader().setMinimumSectionSize(40)  # Minimum width for icon columns
        # Override resize event
        self.msds_records_table.resizeEvent = lambda event: table.resize_columns(self, self.msds_records_table, event)
        self.msds_records_table.verticalHeader().setDefaultSectionSize(44)  # Increased row height
        self.msds_records_table.verticalHeader().setFixedWidth(40)
        self.msds_records_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msds_records_table.horizontalHeader().setFixedHeight(44)  # Match row height
        self.msds_records_table.setShowGrid(False)

    def coa_table_records_init(self):
        self.coa_records_table.setColumnCount(4)
        self.coa_records_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.coa_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.coa_records_table.horizontalHeader().setMinimumSectionSize(40)  # Minimum width for icon columns
        # Override resize event
        self.coa_records_table.resizeEvent = lambda event: table.resize_columns(self, self.coa_records_table, event)
        self.coa_records_table.verticalHeader().setDefaultSectionSize(44)  # Increased row height
        self.coa_records_table.verticalHeader().setFixedWidth(40)
        self.coa_records_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.coa_records_table.horizontalHeader().setFixedHeight(44)  # Match row height
        self.coa_records_table.setShowGrid(False)

    def on_cell_hover(self, row, column):
        table = self.sender()

        # Restore last hovered cell
        if hasattr(self, "last_hovered") and self.last_hovered:
            last_row, last_col = self.last_hovered
            last_item = table.item(last_row, last_col)  # get fresh reference
            if last_item:
                if last_col == 1:
                    last_item.setIcon(QIcon("img/view_icon.png"))  # normal view icon
                elif last_col == 2:
                    last_item.setIcon(QIcon("img/edit_icon.png"))  # normal edit icon
                elif last_col == 3:
                    last_item.setIcon(QIcon("img/delete_icon.png"))  # normal delete icon
            self.last_hovered = None

        # Apply highlight to the current cell
        item = table.item(row, column)
        if item:
            if column == 1:
                item.setIcon(QIcon("img/hover_view_icon.png"))
                self.last_hovered = (row, column)
            elif column == 2:
                item.setIcon(QIcon("img/hover_edit_icon.png"))
                self.last_hovered = (row, column)
            elif column == 3:
                item.setIcon(QIcon("img/hover_delete_icon.png"))
                self.last_hovered = (row, column)
    def msds_cell_clicked(self, row, column):
        msds_id = self.msds_records_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if column == 1:  # view column
            display_text = self.msds_records_table.item(row, 0).text()
            self.open_msds_preview(msds_id, display_text)
        if column == 2:  # edit column
            msds_data_entry.current_msds_id = msds_id  # Store the selected MSDS ID
            msds_data_entry.load_msds_details(self, msds_id)
            # Switch to the MSDS tab
            self.msds_sub_tabs.setCurrentWidget(self.msds_data_entry_tab)
        if column == 3:  # delete column
            confirm = window_alert.show_message(self, "Confirm Deletion",
                                        "Are you sure you want to delete this MSDS record?",
                                        icon_type="question", is_confirmation=True)
            if confirm:
                try:
                    db_con.delete_msds_sheet(msds_id)
                    window_alert.show_message(self, "Deleted", "MSDS record deleted successfully.", icon_type="info")
                except Exception as e:
                    window_alert.show_message(self, "Error", str(e), icon_type="critical")
                finally:
                    table.load_msds_table(self)

    def coa_cell_clicked(self, row, column):
        coa_id = self.coa_records_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if column == 1:  # view column
            display_text = self.coa_records_table.item(row, 0).text()
            self.open_coa_preview(coa_id, display_text)
        if column == 2:  # edit column
            coa_data_entry.current_coa_id = coa_id  # Store the selected COA ID
            coa_data_entry.load_coa_details(self, coa_id)
            # Switch to the COA tab
            self.coa_sub_tabs.setCurrentWidget(self.coa_data_entry_tab)
        if column == 3:  # delete column
            confirm = window_alert.show_message(self, "Confirm Deletion",
                                        "Are you sure you want to delete this Certificate of Analysis record?",
                                        icon_type="question", is_confirmation=True)
            if confirm:
                try:
                    db_con.delete_certificate_of_analysis(coa_id)
                    window_alert.show_message(self, "Deleted", "Certificate of Analysis record deleted successfully.", icon_type="info")
                except Exception as e:
                    window_alert.show_message(self, "Error", str(e), icon_type="critical")
                finally:
                    table.load_coa_table(self)

    def toggle_msds_search_bar(self, index):
        try:
            if index == 0:  # Records tab
                self.msds_search_bar.show()
                msds_data_entry.clear_msds_form(self)
            else:  # Other tabs
                self.msds_search_bar.hide()
        except Exception as e:
            window_alert.show_message(self, "Unexpected Error", f"An error occurred: {str(e)}", icon_type="critical")

    def toggle_coa_search_bar(self, index):
        try:
            if index == 0:  # Records tab
                self.coa_search_bar.show()
                coa_data_entry.clear_coa_form(self)
            else:
                self.coa_search_bar.hide()
        except Exception as e:
            window_alert.show_message(self, "Unexpected Error", f"An error occurred: {str(e)}", icon_type="critical")

    def setup_finished_typing(self, line_edit, callback, delay=800):
        timer = QTimer()
        timer.setSingleShot(True)

        # Connect the timer timeout to the callback
        timer.timeout.connect(callback)

        # Restart timer on every text change
        line_edit.textChanged.connect(lambda: timer.start(delay))

        # Optionally return the timer in case you want to manipulate it later
        return timer

    def check_email(self):
        text = self.email_label_input.text()
        validator = self.email_label_input.validator()
        if validator:
            state = validator.validate(text, 0)[0]
            if state != QRegularExpressionValidator.State.Acceptable and text:
                msg = QMessageBox()
                msg.setWindowTitle("Invalid Email")
                msg.setText("❌ Please enter a valid email address!")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()

    def check_tel_number(self):
        if not self.tel_label_input.hasAcceptableInput():
            msg = QMessageBox()
            msg.setWindowTitle("Invalid Telephone Number")
            msg.setText("❌ Please enter a valid telephone number!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def resize_summary_table(self):
        parent_width = self.coa_data_entry_tab.width()
        table_width = int(parent_width * 0.7)  # 50% width
        self.summary_analysis_table.setFixedWidth(table_width)

    def open_msds_preview(self, msds_id, filename):
        self.msds_widget = FileMSDS()  # create the widget
        self.msds_widget.show_pdf_preview(msds_id, filename)
        self.msds_widget.resize(900, 800)
        self.msds_widget.show()

    def open_coa_preview(self, coa_id, filename):
        self.coa_widget = FileCOA()  # create the widget
        self.coa_widget.show_pdf_preview(coa_id, filename)
        self.coa_widget.resize(900, 800)
        self.coa_widget.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Document Management System")
    window.resize(1000, 800)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
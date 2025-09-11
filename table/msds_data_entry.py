from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem, QFormLayout

from alert import window_alert
from db import db_con

current_msds_id = None  # Global variable to store the current MSDS ID

def load_msds_details(self, msds_id):
    field_result = db_con.get_single_msds_data(msds_id)

    # inputs variable
    self.trade_label_input.setText(str(field_result[1]))
    self.manufactured_label_input.setPlainText(str(field_result[5]))
    self.tel_label_input.setText(str(field_result[6]))
    self.facsimile_label_input.setText(str(field_result[7]))
    self.email_label_input.setText(str(field_result[8]))
    self.composition_input.setPlainText(str(field_result[9]))
    self.hazard_preliminaries_input.setText(str(field_result[10]))
    self.hazard_entry_route_input.setText(str(field_result[11]))
    self.hazard_symptoms_input.setText(str(field_result[12]))
    self.hazard_restrictive_condition_input.setText(str(field_result[13]))
    self.hazard_eyes_input.setText(str(field_result[14]))
    self.hazard_general_note_input.setText(str(field_result[15]))
    self.first_aid_inhalation_input.setText(str(field_result[16]))
    self.first_aid_eyes.setText(str(field_result[17]))
    self.first_aid_skin_input.setText(str(field_result[18]))
    self.first_aid_ingestion_input.setText(str(field_result[19]))
    self.fire_fighting_media_input.setPlainText(str(field_result[20]))
    self.accidental_release_input.setPlainText(str(field_result[21]))
    self.handling_input.setText(str(field_result[22]))
    self.msds_storage_input.setText(str(field_result[23]))
    self.exposure_control_input.setText(str(field_result[24]))
    self.respiratory_protection_input.setText(str(field_result[25]))
    self.hand_protection_input.setText(str(field_result[26]))
    self.eye_protection_input.setText(str(field_result[27]))
    self.skin_protection_input.setText(str(field_result[28]))
    self.appearance_input.setText(str(field_result[29]))
    self.odor_input.setText(str(field_result[30]))
    self.heat_stability_input.setText(str(field_result[31]))
    self.light_fastness_input.setText(str(field_result[32]))
    self.decomposition_input.setText(str(field_result[33]))
    self.flash_point_input.setText(str(field_result[34]))
    self.auto_ignition_input.setText(str(field_result[35]))
    self.explosion_property_input.setText(str(field_result[36]))
    self.solubility_input.setText(str(field_result[37]))
    self.stability_reactivity_input.setPlainText(str(field_result[38]))
    self.toxicological_input.setPlainText(str(field_result[39]))
    self.ecological_input.setPlainText(str(field_result[40]))
    self.disposal_input.setPlainText(str(field_result[41]))
    self.transport_input.setPlainText(str(field_result[42]))
    self.regulatory_input.setPlainText(str(field_result[43]))
    self.msds_shelf_life_input.setText(str(field_result[44]))
    self.other_input.setPlainText(str(field_result[45]))
    self.btn_msds_submit.setText("Update")

def create_form(self):
    header = QLabel("Technical Data and Material Safety")
    header.setStyleSheet("""
        
        font-size: 28px;
        font-weight: 700;
        color: #1a3c6c;
        margin-bottom: 20px;
        text-align: center;
    """)
    section1_header = QLabel("1) Product Identification")
    section1_header.setProperty("class", "sub_title")

    # Create form layout
    form_widget = QWidget()
    form_layout = QFormLayout()
    form_widget.setLayout(form_layout)
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
        QLineEdit, QTextEdit {
            font-size: 14px;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            background-color: #ffffff;
            min-height: 32px;
        }
        QTextEdit {
            min-height: 80px;
            max-height: 80px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4a90e2;
            background-color: #f8fafc;
            box-shadow: 0 0 4px rgba(74, 144, 226, 0.3);
        }
    """)
    form_layout.setHorizontalSpacing(24)
    form_layout.setVerticalSpacing(18)
    form_layout.setContentsMargins(40, 40, 90, 40)

    # Section 1
    form_layout.addRow(section1_header)
    form_layout.addRow(QLabel("Trade Name:"), self.trade_label_input)
    form_layout.addRow(QLabel("Manufactured By:"), self.manufactured_label_input)
    form_layout.addRow(QLabel("Tel No.:"), self.tel_label_input)
    form_layout.addRow(QLabel("Facsimile:"), self.facsimile_label_input)
    form_layout.addRow(QLabel("Email Address:"), self.email_label_input)

    # Section 2
    section2_header = QLabel("2) Composition/Information on Ingredients")
    section2_header.setProperty("class", "sub_title")
    form_layout.addRow(section2_header)
    form_layout.addRow(QLabel("Details:"), self.composition_input)

    # Section 3
    section3_header = QLabel("3) Hazard Information")
    section3_header.setProperty("class", "sub_title")
    section3_label = QLabel("Adverse Human Health Effects")

    form_layout.addRow(section3_header)
    form_layout.addRow(section3_label)
    form_layout.addRow(QLabel("Preliminaries:"), self.hazard_preliminaries_input)
    form_layout.addRow(QLabel("Preliminary route of entry:"), self.hazard_entry_route_input)
    form_layout.addRow(QLabel("Symptoms of Exposure:"), self.hazard_symptoms_input)
    form_layout.addRow(QLabel("Restrictive conditions:"), self.hazard_restrictive_condition_input)
    form_layout.addRow(QLabel("Eyes:"), self.hazard_eyes_input)
    form_layout.addRow(QLabel("General Note:"), self.hazard_general_note_input)

    # Section 4
    section4_header = QLabel("4) First Aid Measures")
    section4_header.setProperty("class", "sub_title")
    form_layout.addRow(section4_header)
    form_layout.addRow(QLabel("Inhalation:"), self.first_aid_inhalation_input)
    form_layout.addRow(QLabel("Eyes:"), self.first_aid_eyes)
    form_layout.addRow(QLabel("Skin:"), self.first_aid_skin_input)
    form_layout.addRow(QLabel("Ingestion:"), self.first_aid_ingestion_input)

    # Section 5
    section5_header = QLabel("5) Fire Fighting Measures")
    section5_header.setProperty("class", "sub_title")
    media_label = QLabel("Extinguishing media: ")

    form_layout.addRow(section5_header)
    form_layout.addRow(media_label, self.fire_fighting_media_input)

    # Section 6
    section6_header = QLabel("6) Accidental Release Measures")
    section6_header.setProperty("class", "sub_title")
    form_layout.addRow(section6_header)
    form_layout.addRow(QLabel("Details:"), self.accidental_release_input)

    # Section 7
    section7_header = QLabel("7) Handling and Storage")
    section7_header.setProperty("class", "sub_title")

    form_layout.addRow(section7_header)
    form_layout.addRow(QLabel("Handling:"), self.handling_input)
    form_layout.addRow(QLabel("Storage:"), self.msds_storage_input)

    # Section 8
    section8_header = QLabel("8) Exposure Controls/Personal Protection")
    section8_header.setProperty("class", "sub_title")

    form_layout.addRow(section8_header)
    form_layout.addRow(QLabel("Exposure Control:"), self.exposure_control_input)
    form_layout.addRow(QLabel("Respiratory Protection:"), self.respiratory_protection_input)
    form_layout.addRow(QLabel("Hand Protection:"), self.hand_protection_input)
    form_layout.addRow(QLabel("Eye Protection:"), self.eye_protection_input)
    form_layout.addRow(QLabel("Skin Protection:"), self.skin_protection_input)

    # Section 9
    section9_header = QLabel("9) Physical & Chemical Properties")
    section9_header.setProperty("class", "sub_title")

    form_layout.addRow(section9_header)
    form_layout.addRow(QLabel("Appearance:"), self.appearance_input)
    form_layout.addRow(QLabel("Odor:"), self.odor_input)
    form_layout.addRow(QLabel("Heat Stability (1-5):"), self.heat_stability_input)
    form_layout.addRow(QLabel("Light fastness (1-8):"), self.light_fastness_input)
    form_layout.addRow(QLabel("Decomposition (°C):"), self.decomposition_input)
    form_layout.addRow(QLabel("Flash Point (°C):"), self.flash_point_input)
    form_layout.addRow(QLabel("Auto Ignition (°C):"), self.auto_ignition_input)
    form_layout.addRow(QLabel("Explosion Property:"), self.explosion_property_input)
    form_layout.addRow(QLabel("Solubility (Water):"), self.solubility_input)

    # Section 10
    section10_header = QLabel("10) Stability & Reactivity")
    section10_header.setProperty("class", "sub_title")

    form_layout.addRow(section10_header)
    form_layout.addRow(QLabel("Details:"), self.stability_reactivity_input)

    # Section 11
    section11_header = QLabel("11) Toxicological Information")
    section11_header.setProperty("class", "sub_title")
    form_layout.addRow(section11_header)
    form_layout.addRow(QLabel("Details:"), self.toxicological_input)

    # Section 12-17
    section12_header = QLabel("12) Ecological Information")
    section12_header.setProperty("class", "sub_title")
    section13_header = QLabel("13) Disposal")
    section13_header.setProperty("class", "sub_title")
    section14_header = QLabel("14) Transport Information")
    section14_header.setProperty("class", "sub_title")
    section15_header = QLabel("15) Regulatory Information")
    section15_header.setProperty("class", "sub_title")
    section16_header = QLabel("16) Shelf-Life")
    section16_header.setProperty("class", "sub_title")
    section17_header = QLabel("17) Other Information")
    section17_header.setProperty("class", "sub_title")

    form_layout.addRow(section12_header)
    form_layout.addRow(QLabel("Details:"), self.ecological_input)
    form_layout.addRow(section13_header)
    form_layout.addRow(QLabel("Details:"), self.disposal_input)
    form_layout.addRow(section14_header)
    form_layout.addRow(QLabel("Details:"), self.transport_input)
    form_layout.addRow(section15_header)
    form_layout.addRow(QLabel("Details:"), self.regulatory_input)
    form_layout.addRow(section16_header)
    form_layout.addRow(QLabel("Details:"), self.msds_shelf_life_input)
    form_layout.addRow(section17_header)
    form_layout.addRow(QLabel("Details:"), self.other_input)
    form_layout.addRow(form_btn(self))

    # Center the header
    header_layout = QHBoxLayout()
    header_layout.addStretch()
    header_layout.addWidget(header)
    header_layout.addStretch()
    self.msds_form_layout.addLayout(header_layout)
    self.msds_form_layout.addWidget(form_widget)

def form_btn(self):
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
        QPushButton:hover {
            background-color: #45a049;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        QPushButton:pressed {
            background-color: #388e3c;
        }
        QPushButton:focus {
            outline: none;
            border: 2px solid #4a90e2;
        }
    """
    self.btn_msds_submit.setStyleSheet(button_style)
    submit_button_row = QHBoxLayout()
    submit_button_row.addStretch()
    submit_button_row.addStretch()
    submit_button_row.addWidget(self.btn_msds_submit)
    return submit_button_row

def clear_msds_form(self):
    """Clear all input fields and the summary table."""
    global current_msds_id
    try:
        current_msds_id = None  # Reset the global MSDS ID
        # Clear QLineEdit/QTextEdit fields
        self.trade_label_input.clear()
        self.manufactured_label_input.clear()

        # Stop all typing timers
        self.tel_label_timer.stop()
        self.facsimile_label_timer.stop()
        self.email_label_timer.stop()

        # Clear fields safely
        for widget in [
            self.tel_label_input,
            self.facsimile_label_input,
            self.email_label_input,
            self.trade_label_input,
            self.manufactured_label_input,
            self.composition_input,
            self.hazard_preliminaries_input,
            self.hazard_entry_route_input,
            self.hazard_symptoms_input,
            self.hazard_restrictive_condition_input,
            self.hazard_eyes_input,
            self.hazard_general_note_input,
            self.first_aid_inhalation_input,
            self.first_aid_eyes,
            self.first_aid_skin_input,
            self.first_aid_ingestion_input,
            self.fire_fighting_media_input,
            self.accidental_release_input,
            self.handling_input,
            self.msds_storage_input,
            self.exposure_control_input,
            self.respiratory_protection_input,
            self.hand_protection_input,
            self.eye_protection_input,
            self.skin_protection_input,
            self.appearance_input,
            self.odor_input,
            self.heat_stability_input,
            self.light_fastness_input,
            self.decomposition_input,
            self.flash_point_input,
            self.auto_ignition_input,
            self.explosion_property_input,
            self.solubility_input,
            self.stability_reactivity_input,
            self.toxicological_input,
            self.ecological_input,
            self.disposal_input,
            self.transport_input,
            self.regulatory_input,
            self.msds_shelf_life_input,
            self.other_input
        ]:
            widget.blockSignals(True)
            widget.clear()
            widget.blockSignals(False)

        self.btn_msds_submit.setText("Submit")
    except Exception as e:
        window_alert.show_message(self, "Unexpected Error", f"An error occurred: {str(e)}", icon_type="critical")


from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem, QFormLayout


def create_form(self):
    header = QLabel("Technical Data and Material Safety")
    header.setStyleSheet("font-size: 18px; font-weight: bold; font-size: 24px;")
    section1_header = QLabel("1) Product Identification")
    section1_header.setProperty("class", "sub_title")

    # Create form layout
    form_widget = QWidget()
    form_layout = QFormLayout()
    form_widget.setLayout(form_layout)
    form_widget.setStyleSheet(""" 
        QLabel {
            margin-left: 60px;
            font-size: 16px;
        }
        QLineEdit, QTextEdit {
            font-size: 16px;
            padding: 4px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .sub_title {
            margin-left: 0;
            font-size: 20px;
            font-weight: bold;
            margin-top: 12px;
            margin-bottom: 8px;
        }
        
    """)
    form_layout.setHorizontalSpacing(20)
    form_layout.setVerticalSpacing(12)
    form_layout.setContentsMargins(20, 20, 70, 20)

    #Section 1
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
    form_layout.addRow(QLabel("Details:"),self.toxicological_input)

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

    self.msds_form_layout.addWidget(header)
    self.msds_form_layout.addWidget(form_widget)


def form_btn(self):
    self.msds_btn_layout.addStretch()
    self.msds_btn_layout.addWidget(self.btn_msds_submit)

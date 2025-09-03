
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTabWidget, \
    QTableWidget, QLineEdit, QHeaderView, QTableWidgetItem


def form_section1(self):
    header = QLabel("Technical Data and Material Safety")
    trade_layout = QHBoxLayout()
    manufacture_layout = QHBoxLayout()
    tel_layout = QHBoxLayout()
    facsimile_layout = QHBoxLayout()
    email_layout = QHBoxLayout()

    section1_header = QLabel("1) Product Identification")
    trade_label = QLabel("Trade Name: ")
    manufactured_label = QLabel("Trade Name: ")
    tel_label = QLabel("Tel No.: ")
    facsimile_label = QLabel("Facsimile: ")
    email_label = QLabel("Email Address: ")

    trade_layout.addWidget(trade_label)
    trade_layout.addWidget(self.trade_label_input)
    manufacture_layout.addWidget(manufactured_label)
    manufacture_layout.addWidget(self.manufactured_label_input)
    tel_layout.addWidget(tel_label)
    tel_layout.addWidget(self.tel_label_input)
    facsimile_layout.addWidget(facsimile_label)
    facsimile_layout.addWidget(self.facsimile_label_input)
    email_layout.addWidget(email_label)
    email_layout.addWidget(self.email_label_input)

    self.section1_layout.addWidget(header)
    self.section1_layout.addWidget(section1_header)
    self.section1_layout.addLayout(trade_layout)
    self.section1_layout.addLayout(manufacture_layout)
    self.section1_layout.addLayout(tel_layout)
    self.section1_layout.addLayout(facsimile_layout)
    self.section1_layout.addLayout(email_layout)


def form_section2(self):
    section2_header = QLabel("2) Composition/Information on Ingredients")
    self.section2_layout.addWidget(section2_header)
    self.section2_layout.addWidget(self.composition_input)


def form_section3(self):
    preliminaries_layout = QHBoxLayout()
    entry_route_layout = QHBoxLayout()
    symptoms_layout = QHBoxLayout()
    restrictive_condition_layout = QHBoxLayout()
    eyes_layout = QHBoxLayout()
    general_note_layout = QHBoxLayout()

    section3_header = QLabel("3) Hazard Information")
    label = QLabel('Adverse Human Health Effects')
    preliminaries_label = QLabel("Preliminaries: ")
    entry_route_label = QLabel("Preliminary route of entry: ")
    symptoms_label = QLabel("Symptoms of Exposure: ")
    restrictive_condition_label = QLabel("Restrictive conditions: ")
    eyes_label = QLabel("Eyes: ")
    general_note_label = QLabel("General Note: ")

    preliminaries_layout.addWidget(preliminaries_label)
    preliminaries_layout.addWidget(self.hazard_preliminaries_input)
    entry_route_layout.addWidget(entry_route_label)
    entry_route_layout.addWidget(self.hazard_entry_route_input)
    symptoms_layout.addWidget(symptoms_label)
    symptoms_layout.addWidget(self.hazard_symptoms_input)
    restrictive_condition_layout.addWidget(restrictive_condition_label)
    restrictive_condition_layout.addWidget(self.hazard_restrictive_condition_input)
    eyes_layout.addWidget(eyes_label)
    eyes_layout.addWidget(self.hazard_eyes_input)
    general_note_layout.addWidget(general_note_label)
    general_note_layout.addWidget(self.hazard_general_note_input)

    self.section3_layout.addWidget(section3_header)
    self.section3_layout.addWidget(label)
    self.section3_layout.addLayout(preliminaries_layout)
    self.section3_layout.addLayout(entry_route_layout)
    self.section3_layout.addLayout(symptoms_layout)
    self.section3_layout.addLayout(restrictive_condition_layout)
    self.section3_layout.addLayout(eyes_layout)
    self.section3_layout.addLayout(general_note_layout)


def form_section4(self):
    inhalation_layout = QHBoxLayout()
    eyes_layout = QHBoxLayout()
    skin_layout = QHBoxLayout()
    ingestion_layout = QHBoxLayout()

    section4_header = QLabel("4) First Aid Measures")
    inhalation_label = QLabel("Inhalation: ")
    eyes_label = QLabel("Eyes: ")
    skin_label = QLabel("Skin: ")
    ingestion_label = QLabel("Ingestion: ")

    inhalation_layout.addWidget(inhalation_label)
    inhalation_layout.addWidget(self.first_aid_inhalation_input)
    eyes_layout.addWidget(eyes_label)
    eyes_layout.addWidget(self.first_aid_eyes)
    skin_layout.addWidget(skin_label)
    skin_layout.addWidget(self.first_aid_skin_input)
    ingestion_layout.addWidget(ingestion_label)
    ingestion_layout.addWidget(self.first_aid_ingestion_input)

    self.section4_layout.addWidget(section4_header)
    self.section4_layout.addLayout(inhalation_layout)
    self.section4_layout.addLayout(eyes_layout)
    self.section4_layout.addLayout(skin_layout)
    self.section4_layout.addLayout(ingestion_layout)


def form_section5(self):
    fire_fighting_layout = QHBoxLayout()

    section5_header = QLabel("5) Fire Fighting Measures")
    media_label = QLabel("Extinguishing media: ")

    self.section5_layout.addWidget(section5_header)
    self.section5_layout.addWidget(media_label)
    self.section5_layout.addWidget(self.fire_fighting_media_input)


def form_section6(self):

    section6_header = QLabel("6) Accidental Release Measures")

    self.section6_layout.addWidget(section6_header)
    self.section6_layout.addWidget(self.accidental_release_input)

def form_section7(self):
    handling_layout = QHBoxLayout()
    storage_layout = QHBoxLayout()

    section7_header = QLabel("7) Handling and Storage")
    handling_label = QLabel("Handling: ")
    storage_label = QLabel("Storage: ")

    self.section7_layout.addWidget(section7_header)
    handling_layout.addWidget(handling_label)
    handling_layout.addWidget(self.handling_input)
    storage_layout.addWidget(storage_label)
    storage_layout.addWidget(self.msds_storage_input)

    self.section7_layout.addLayout(handling_layout)
    self.section7_layout.addLayout(storage_layout)

def form_section8(self):
    exposure_layout = QHBoxLayout()
    respiratory_layout = QHBoxLayout()
    hand_protection_layout = QHBoxLayout()
    eye_protection_layout = QHBoxLayout()
    skin_protection_layout = QHBoxLayout()

    section8_header = QLabel("8) Exposure Controls/Personal Protection")
    exposure_label = QLabel("Exposure Control: ")
    respiratory_label = QLabel("Respiratory Protection: ")
    hand_label = QLabel("Hand Protection: ")
    eye_label = QLabel("Eye Protection: ")
    skin_label = QLabel("Skin Protection: ")

    exposure_layout.addWidget(exposure_label)
    exposure_layout.addWidget(self.exposure_control_input)
    respiratory_layout.addWidget(respiratory_label)
    respiratory_layout.addWidget(self.respiratory_protection_input)
    hand_protection_layout.addWidget(hand_label)
    hand_protection_layout.addWidget(self.hand_protection_input)
    eye_protection_layout.addWidget(eye_label)
    eye_protection_layout.addWidget(self.eye_protection_input)
    skin_protection_layout.addWidget(skin_label)
    skin_protection_layout.addWidget(self.skin_protection_input)

    self.section8_layout.addWidget(section8_header)
    self.section8_layout.addLayout(exposure_layout)
    self.section8_layout.addLayout(respiratory_layout)
    self.section8_layout.addLayout(hand_protection_layout)
    self.section8_layout.addLayout(eye_protection_layout)
    self.section8_layout.addLayout(skin_protection_layout)


def form_section9(self):
    appearance_layout = QHBoxLayout()
    odor_layout = QHBoxLayout()
    heat_stability_layout = QHBoxLayout()
    light_fastness_layout = QHBoxLayout()
    decomposition_layout = QHBoxLayout()
    flash_point_layout = QHBoxLayout()
    auto_ignition_layout = QHBoxLayout()
    explosion_property_layout = QHBoxLayout()
    solubility_layout = QHBoxLayout()

    section9_header = QLabel("9) Physical & Chemical Properties")
    appearance_label = QLabel("Appearance: ")
    odor_label = QLabel("Odor: ")
    heat_stability_label = QLabel("Heat Stability (1-5): ")
    light_fastness_label = QLabel("Light fastness (1-8): ")
    decomposition_label = QLabel("Decomposition (°C): ")
    flash_point_label = QLabel("Flash Point (°C): ")
    auto_ignition_label = QLabel("Auto Ignition (°C): ")
    explosion_property_label = QLabel("Explosion Property: ")
    solubility_label = QLabel("Solubility (Water): ")

    appearance_layout.addWidget(appearance_label)
    appearance_layout.addWidget(self.appearance_input)
    odor_layout.addWidget(odor_label)
    odor_layout.addWidget(self.odor_input)
    heat_stability_layout.addWidget(heat_stability_label)
    heat_stability_layout.addWidget(self.heat_stability_input)
    light_fastness_layout.addWidget(light_fastness_label)
    light_fastness_layout.addWidget(self.light_fastness_input)
    decomposition_layout.addWidget(decomposition_label)
    decomposition_layout.addWidget(self.decomposition_input)
    flash_point_layout.addWidget(flash_point_label)
    flash_point_layout.addWidget(self.flash_point_input)
    auto_ignition_layout.addWidget(auto_ignition_label)
    auto_ignition_layout.addWidget(self.auto_ignition_input)
    explosion_property_layout.addWidget(explosion_property_label)
    explosion_property_layout.addWidget(self.explosion_property_input)
    solubility_layout.addWidget(solubility_label)
    solubility_layout.addWidget(self.solubility_input)

    self.section9_layout.addWidget(section9_header)
    self.section9_layout.addLayout(appearance_layout)
    self.section9_layout.addLayout(odor_layout)
    self.section9_layout.addLayout(heat_stability_layout)
    self.section9_layout.addLayout(light_fastness_layout)
    self.section9_layout.addLayout(decomposition_layout)
    self.section9_layout.addLayout(flash_point_layout)
    self.section9_layout.addLayout(auto_ignition_layout)
    self.section9_layout.addLayout(explosion_property_layout)
    self.section9_layout.addLayout(solubility_layout)


def form_section10(self):
    section10_header = QLabel("10) Stability & Reactivity")

    self.section10_layout.addWidget(section10_header)
    self.section10_layout.addWidget(self.stability_reactivity_input)


def form_section11(self):
    section11_header = QLabel("11) Toxicological Information")

    self.section11_layout.addWidget(section11_header)
    self.section11_layout.addWidget(self.toxicological_input)


def form_section12(self):
    section12_header = QLabel("12) Ecological Information")

    self.section12_layout.addWidget(section12_header)
    self.section12_layout.addWidget(self.ecological_input)

def form_section13(self):
    section13_header = QLabel("13) Disposal")

    self.section13_layout.addWidget(section13_header)
    self.section13_layout.addWidget(self.disposal_input)

def form_section14(self):
    section14_header = QLabel("14) Transport Information")

    self.section14_layout.addWidget(section14_header)
    self.section14_layout.addWidget(self.transport_input)

def form_section15(self):
    section15_header = QLabel("15) Regulatory Information")

    self.section15_layout.addWidget(section15_header)
    self.section15_layout.addWidget(self.regulatory_input)


def form_section16(self):
    section16_header = QLabel("16) Shelf-Life")

    self.section16_layout.addWidget(section16_header)
    self.section16_layout.addWidget(self.msds_shelf_life_input)


def form_section17(self):
    section17_header = QLabel("17) Other Information")

    self.section17_layout.addWidget(section17_header)
    self.section17_layout.addWidget(self.other_input)


def from_btn(self):
    self.msds_btn_layout.addStretch()
    self.msds_btn_layout.addWidget(self.btn_msds_submit)

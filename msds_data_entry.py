<<<<<<< HEAD
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from db import db_con
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
    storage_layout.addWidget(self.storage_input)

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

    self.section8_layout.addWidget(exposure_label)
    exposure_layout.addWidget(section8_header)
    exposure_layout.addWidget(self.exposure_control_input)
    respiratory_layout.addWidget(respiratory_label)
    respiratory_layout.addWidget(self.respiratory_protection_input)
    hand_protection_layout.addWidget(hand_label)
    hand_protection_layout.addWidget(self.hand_protection_input)
    eye_protection_layout.addWidget(eye_label)
    eye_protection_layout.addWidget(self.eye_protection_input)
    skin_protection_layout.addWidget(skin_label)
    skin_protection_layout.addWidget(self.skin_protection_input)

    self.section8_layout.addLayout(exposure_layout)
    self.section8_layout.addLayout(respiratory_layout)
    self.section8_layout.addLayout(hand_protection_layout)
    self.section8_layout.addLayout(eye_protection_layout)
    self.section8_layout.addLayout(skin_protection_layout)
=======
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from db import db_con
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
    storage_layout.addWidget(self.storage_input)

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

    self.section8_layout.addWidget(exposure_label)
    exposure_layout.addWidget(section8_header)
    exposure_layout.addWidget(self.exposure_control_input)
    respiratory_layout.addWidget(respiratory_label)
    respiratory_layout.addWidget(self.respiratory_protection_input)
    hand_protection_layout.addWidget(hand_label)
    hand_protection_layout.addWidget(self.hand_protection_input)
    eye_protection_layout.addWidget(eye_label)
    eye_protection_layout.addWidget(self.eye_protection_input)
    skin_protection_layout.addWidget(skin_label)
    skin_protection_layout.addWidget(self.skin_protection_input)

    self.section8_layout.addLayout(exposure_layout)
    self.section8_layout.addLayout(respiratory_layout)
    self.section8_layout.addLayout(hand_protection_layout)
    self.section8_layout.addLayout(eye_protection_layout)
    self.section8_layout.addLayout(skin_protection_layout)
>>>>>>> 4b2f374a4a5590bcfa2a0d63226a93905a83d47a

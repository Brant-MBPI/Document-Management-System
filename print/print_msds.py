from PIL.ImageQt import QPixmap
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pdf2image import convert_from_path
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from pdf2image import convert_from_path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton


class FileMSDS(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # PDF Document + Viewer
        self.pdf_doc = QPdfDocument(self)
        self.pdf_viewer = QPdfView(self)
        self.pdf_viewer.setDocument(self.pdf_doc)

        # Put inside scroll (optional if you want scrolling)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.pdf_viewer)

        self.layout.addWidget(QPushButton("save"))
        self.layout.addWidget(self.scroll)
    def generate_pdf(self, filename):
        # Create PDF

        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(name="SectionHeader", fontSize=12, leading=14, spaceAfter=6, spaceBefore=12, bold=True))
        styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=14, spaceAfter=6))

        elements = []

        # Title
        elements.append(Paragraph("<b>TECHNICAL DATA AND MATERIAL SAFETY DATA SHEET</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Sections (copied from your PDF)
        sections = [
            ("1) Product Identification",
             """
             <b>Trade Name</b> : Masterbatch White WA17857E<br/>
             <b>Manufactured by</b> : Masterbatch Philippines, Inc.<br/>
             24 Diamond Road, Caloocan Industrial Subdivision,<br/>
             Bo. Kaybiga, Caloocan City, Philippines<br/><br/>
             <b>Tel No</b> : (632) 87088681<br/>
             <b>Facsimile</b> : (632) 83747085<br/>
             <b>Email Address</b> : sales@polycolor.biz
             """),

            ("2) Composition / Information on Ingredients",
             "The preparation consists of organic pigments, polyolefin resin, and other additives."),

            ("3) Hazard Information",
             "No known harmful effects to human lives or to the environment."),

            ("4) First Aid Measures",
             "• Inhalation - N/A<br/>"
             "• Eyes - N/A<br/>"
             "• Skin - N/A<br/>"
             "• Ingestion - N/A"),

            ("5) Fire Fighting Measures",
             "• Water spray, dry powder, foam, carbon dioxide"),

            ("6) Accidental Release Measures",
             "Use any mechanical means to remove pellet. Prevent entry to natural waterways."),

            ("7) Handling / Storage",
             "Store in a dry place and shaded area. Close bag after use to prevent moisture intake & soiling."),

            ("8) Exposure Controls / Personal Protection",
             "• Exposure Control - Generally, handle in accordance with good industrial hygiene and safety practices.<br/>"
             "• Respiratory Protection - None<br/>"
             "• Hand protection - None<br/>"
             "• Eye Protection - None<br/>"
             "• Skin Protection - None"),

            ("9) Physical & Chemical Properties",
             "Appearance : White pellet form<br/>"
             "Odor : Odorless<br/>"
             "Packaging : 25 kgs.<br/>"
             "Carrier Material : Polyolefin resin<br/>"
             "Resin Suitability : Polyolefin<br/>"
             "Light fastness (1-8) : 7-8<br/>"
             "Heat Stability (1-5) : 4-5<br/>"
             "Non-Toxicity : Non-toxic, colorant contains no heavy metal<br/>"
             "Flash Point : N/A<br/>"
             "Auto Ignition : N/A<br/>"
             "Explosion Property : N/A<br/>"
             "Solubility (Water) : Insoluble"),

            ("10) Stability & Reactivity",
             "This product is chemically stable and non-reactive.<br/><br/>"
             "<b>Conditions to avoid</b> : None<br/>"
             "<b>Materials to avoid</b> : None<br/>"
             "<b>Hazardous decomposition</b> : None"),

            ("11) Toxicological Information",
             "This product is non-toxic and physiologically harmless."),

            ("12) Ecological Information",
             "No known harmful effects to human lives or to the environment."),

            ("13) Disposal",
             "If recycling is not practicable, dispose in compliance with local regulation."),

            ("14) Transport Information",
             "This material is not classified as a dangerous good by the International Transport regulation."),

            ("15) Regulatory Information",
             "This product is not classified in the list of controlled substances implemented by the government."),

            ("16) Shelf-Life",
             "Twelve months from date of production when the product is stored in unbroken packaging."),

            ("17) Other Information",
             "None")
        ]

        # Add sections
        for header, content in sections:
            elements.append(Paragraph(f"<b>{header}</b>", styles["SectionHeader"]))
            elements.append(Paragraph(content, styles["NormalText"]))

        # Build PDF
        doc.build(elements)
        return filename

    def show_pdf_preview(self, filename: str):
        self.pdf_doc.load(filename)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def generate_and_preview(self):
        pdf_file = self.generate_pdf("test.pdf")
        self.show_pdf_preview(pdf_file)

from PIL.ImageQt import QPixmap
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
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

        # Scrollable view with multiple pages
        self.pdf_viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

        # Add to layout
        generate_btn = QPushButton("Generate & Preview PDF")
        generate_btn.clicked.connect(self.generate_and_preview)
        self.layout.addWidget(generate_btn)
        self.layout.addWidget(self.pdf_viewer)

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
            ParagraphStyle(name="SectionHeader", fontSize=14, leading=14, spaceAfter=12, spaceBefore=12, bold=True))
        styles.add(ParagraphStyle(name="NormalText", fontSize=12, leading=14, spaceAfter=6))
        styles.add(ParagraphStyle(name="TableText", fontSize=10, leading=12))
        IndentedText = ParagraphStyle(
            'IndentedText',
            parent=styles['NormalText'],  # inherit font size, leading, etc.
            leftIndent=40  # indent in points
        )
        content = []
        page_width = letter[0] - 50 - 50  # letter[0] is width, subtract left/right margins
        table_width = 0.90 * page_width  # make table 85% of page width
        col_widths = [0.3 * table_width, 0.05 * table_width, 0.65 * table_width]

        # Title
        content.append(Paragraph("TECHNICAL DATA AND MATERIAL SAFETY DATA SHEET", styles['Title']))
        content.append(Spacer(1, 12))

        # Section 1
        content.append(Paragraph("1) Product Identification", styles['SectionHeader']))
        section1_content = [
            [Paragraph('Trade Name', styles['NormalText']), ':', Paragraph('Masterbatch White WA17857E', styles['NormalText'])],
            [Paragraph('Manufactured by', styles['NormalText']), ':', Paragraph('Masterbatch Philippines, Inc.', styles['NormalText'])],
            [Paragraph('Address', styles['NormalText']), ':', Paragraph('24 Diamond Road, Caloocan Industrial Subdivision, Bo. Kaybiga, Caloocan City, Philippines',styles['NormalText'])],
            [Paragraph('Tel No', styles['NormalText']), ':', Paragraph('(632) 87088681', styles['NormalText'])],
            [Paragraph('Facsimile', styles['NormalText']), ':', Paragraph('(632) 83747085', styles['NormalText'])],
            [Paragraph('Email Address', styles['NormalText']), ':', Paragraph('sales@polycolor.biz', styles['NormalText'])]
        ]

        # Create the table
        table = Table(section1_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)  # Adjust column widths as needed

        # Apply styles
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # left-align all columns
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # center-align the middle ":"
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey)
        ]))
        # Add the table to the content
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 2
        content.append(Paragraph("2) Composition / Information on Ingredients", styles['SectionHeader']))
        content.append(Paragraph("The preparation consists of organic pigments, polyolefin resin, and other additives.",
                                 IndentedText))
        content.append(Spacer(1, 12))

        # Section 3
        content.append(Paragraph("3) Hazard Information", styles['SectionHeader']))
        content.append(Paragraph("No known harmful effects to human lives or to the environment.", IndentedText))
        content.append(Spacer(1, 12))

        # Section 4
        content.append(Paragraph("4) First Aid Measures", styles['SectionHeader']))
        content.append(Paragraph(
            "• Inhalation - N/A<br/>"
            "• Eyes - N/A<br/>"
            "• Skin - N/A<br/>"
            "• Ingestion - N/A", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 5
        content.append(Paragraph("5) Fire Fighting Measures", styles['SectionHeader']))
        content.append(Paragraph("• Water spray, dry powder, foam, carbon dioxide", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 6
        content.append(Paragraph("6) Accidental Release Measures", styles['SectionHeader']))
        content.append(Paragraph("Use any mechanical means to remove pellet. Prevent entry to natural waterways.",
                                 styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 7
        content.append(Paragraph("7) Handling/ Storage", styles['SectionHeader']))
        content.append(
            Paragraph("Store in a dry place and shaded area. Close bag after use to prevent moisture intake & soiling.",
                      styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 8
        content.append(Paragraph("8) Exposure Controls/ Personal Protection", styles['SectionHeader']))
        content.append(Paragraph(
            "• Exposure Control - Generally, handle in accordance with good industrial hygiene and safety practices.<br/>"
            "• Respiratory Protection - None<br/>"
            "• Hand protection - None<br/>"
            "• Eye Protection - None<br/>"
            "• Skin Protection - None", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 9
        content.append(Paragraph("9) Physical & Chemical Properties", styles['SectionHeader']))
        content.append(Paragraph(
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
            "Solubility (Water) : Insoluble", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 10
        content.append(Paragraph("10) Stability & Reactivity", styles['SectionHeader']))
        content.append(Paragraph(
            "This product is chemically stable and non-reactive.<br/>"
            "Conditions to avoid : None<br/>"
            "Materials to avoid : None<br/>"
            "Hazardous decomposition : None", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 11
        content.append(Paragraph("11) Toxicological Information", styles['SectionHeader']))
        content.append(Paragraph("This product is non-toxic and physiologically harmless.", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 12
        content.append(Paragraph("12) Ecological Information", styles['SectionHeader']))
        content.append(Paragraph("No known harmful effects to human lives or to the environment.", styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 13
        content.append(Paragraph("13) Disposal", styles['SectionHeader']))
        content.append(Paragraph("If recycling is not practicable, dispose in compliance with local regulation.",
                                 styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 14
        content.append(Paragraph("14) Transport Information", styles['SectionHeader']))
        content.append(
            Paragraph("This material is not classified as a dangerous good by the International Transport regulation.",
                      styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 15
        content.append(Paragraph("15) Regulatory Information", styles['SectionHeader']))
        content.append(Paragraph(
            "This product is not classified in the list of controlled substances implemented by the government.",
            styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 16
        content.append(Paragraph("16) Shelf-Life", styles['SectionHeader']))
        content.append(
            Paragraph("Twelve months from date of production when the product is stored in unbroken packaging.",
                      styles['NormalText']))
        content.append(Spacer(1, 12))

        # Section 17
        content.append(Paragraph("17) Other Information", styles['SectionHeader']))
        content.append(Paragraph("None", styles['NormalText']))
        content.append(PageBreak())

        doc.build(content)
        return filename

    def show_pdf_preview(self, filename: str):
        self.pdf_doc.load(filename)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def generate_and_preview(self):
        pdf_file = self.generate_pdf("test.pdf")
        self.show_pdf_preview(pdf_file)

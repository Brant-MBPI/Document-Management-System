from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
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
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout


class FileMSDS(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        # PDF Document + Viewer
        self.pdf_doc = QPdfDocument(self)
        self.pdf_viewer = QPdfView(self)
        self.pdf_viewer.setDocument(self.pdf_doc)

        # Scrollable view with multiple pages
        self.pdf_viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

        # Set the viewer widget to match letter size (8.5x11 inches at 96 DPI)
        dpi = 96
        letter_width = int(8.5 * dpi)  # 816 px
        self.pdf_viewer.setFixedWidth(letter_width)

        # Add Generate button at the top
        generate_btn = QPushButton("Download")
        generate_btn.clicked.connect(self.generate_and_preview)
        main_layout.addWidget(generate_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        # Center the viewer using a horizontal layout
        viewer_container = QHBoxLayout()
        viewer_container.addStretch(1)  # left stretch
        viewer_container.addWidget(self.pdf_viewer)
        viewer_container.addStretch(1)  # right stretch
        main_layout.addLayout(viewer_container)


    def generate_pdf(self, filename):
        # Create PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(name="SectionHeader", fontSize=14, leading=14, spaceAfter=12, spaceBefore=6, bold=True))
        styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=14, spaceAfter=4))
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
            [Paragraph('Manufactured by', styles['NormalText']), ':', Paragraph('Masterbatch Philippines, Inc. 24 Diamond Road, Caloocan Industrial Subdivision, Bo. Kaybiga, Caloocan City, Philippines', styles['NormalText'])],
            [Paragraph('Tel No', styles['NormalText']), ':', Paragraph('(632) 87088681', styles['NormalText'])],
            [Paragraph('Facsimile', styles['NormalText']), ':', Paragraph('(632) 83747085', styles['NormalText'])],
            [Paragraph('Email Address', styles['NormalText']), ':', Paragraph('sales@polycolor.biz', styles['NormalText'])]
        ]

        # Create the table
        table = Table(section1_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)  # Adjust column widths as needed

        # Apply styles
        def table_style(table ):
            return table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # left-align all columns
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # center-align the middle ":"
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.Color(0.85, 0.85, 0.85))
            ]))
        table_style(table)
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
        section4_content = [
            [Paragraph('• Inhalation', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
            [Paragraph('• Eyes', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
            [Paragraph('• Skin', styles['NormalText']), ':', Paragraph('N/A',styles['NormalText'])],
            [Paragraph('• Ingestion', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
           ]

        # Create the table
        table = Table(section4_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 5
        content.append(Paragraph("5) Fire Fighting Measures", styles['SectionHeader']))
        content.append(Paragraph("• Water spray, dry powder, foam, carbon dioxide", IndentedText))
        content.append(Spacer(1, 12))

        # Section 6
        content.append(Paragraph("6) Accidental Release Measures", styles['SectionHeader']))
        content.append(Paragraph("Use any mechanical means to remove pellet. Prevent entry to natural waterways.",
                                 IndentedText))
        content.append(Spacer(1, 12))

        # Section 7
        content.append(Paragraph("7) Handling/ Storage", styles['SectionHeader']))
        content.append(
            Paragraph("Store in a dry place and shaded area. Close bag after use to prevent moisture intake & soiling.",
                      IndentedText))
        content.append(Spacer(1, 12))

        # Section 8
        content.append(Paragraph("8) Exposure Controls/ Personal Protection", styles['SectionHeader']))
        section8_content = [
            [Paragraph('Exposure Control', styles['NormalText']), ':',
             Paragraph('Generally, handle in accordance with good industrial hygiene and safety practices.',styles['NormalText'])],
            [Paragraph('Respiratory Protection', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])],
            [Paragraph('Hand Protection', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])],
            [Paragraph('Eye Protection', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])],
            [Paragraph('Skin Protection', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])]
        ]
        table = Table(section8_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 9
        content.append(Paragraph("9) Physical & Chemical Properties", styles['SectionHeader']))
        section9_content = [
            [Paragraph('Appearance', styles['NormalText']), ':', Paragraph('White pellet form', styles['NormalText'])],
            [Paragraph('Odor', styles['NormalText']), ':', Paragraph('Odorless', styles['NormalText'])],
            [Paragraph('Packaging', styles['NormalText']), ':', Paragraph('25 kgs.', styles['NormalText'])],
            [Paragraph('Carrier Material', styles['NormalText']), ':',
             Paragraph('Polyolefin resin', styles['NormalText'])],
            [Paragraph('Resin Suitability', styles['NormalText']), ':', Paragraph('Polyolefin', styles['NormalText'])],
            [Paragraph('Light fastness (1-8)', styles['NormalText']), ':', Paragraph('7-8', styles['NormalText'])],
            [Paragraph('Heat Stability (1-5)', styles['NormalText']), ':', Paragraph('4-5', styles['NormalText'])],
            [Paragraph('Non-Toxicity', styles['NormalText']), ':',
             Paragraph('Non-toxic, colorant contains no heavy metal', styles['NormalText'])],
            [Paragraph('Flash Point', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
            [Paragraph('Auto Ignition', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
            [Paragraph('Explosion Property', styles['NormalText']), ':', Paragraph('N/A', styles['NormalText'])],
            [Paragraph('Solubility (Water)', styles['NormalText']), ':', Paragraph('Insoluble', styles['NormalText'])]
        ]

        # Create the table
        table = Table(section9_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 10
        content.append(Paragraph("10) Stability & Reactivity", styles['SectionHeader']))
        section10_content = [
            [Paragraph('Product Stability', styles['NormalText']), ':',
             Paragraph('Chemically stable and non-reactive', styles['NormalText'])],
            [Paragraph('Conditions to avoid', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])],
            [Paragraph('Materials to avoid', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])],
            [Paragraph('Hazardous decomposition', styles['NormalText']), ':', Paragraph('None', styles['NormalText'])]
        ]
        table = Table(section10_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 11
        content.append(Paragraph("11) Toxicological Information", styles['SectionHeader']))
        content.append(Paragraph("This product is non-toxic and physiologically harmless.", IndentedText))
        content.append(Spacer(1, 12))

        # Section 12
        content.append(Paragraph("12) Ecological Information", styles['SectionHeader']))
        content.append(Paragraph("No known harmful effects to human lives or to the environment.", IndentedText))
        content.append(Spacer(1, 12))
        # Section 13
        content.append(Paragraph("13) Disposal", styles['SectionHeader']))
        content.append(Paragraph("If recycling is not practicable, dispose in compliance with local regulation.",
                                 IndentedText))
        content.append(Spacer(1, 12))

        # Section 14
        content.append(Paragraph("14) Transport Information", styles['SectionHeader']))
        content.append(
            Paragraph("This material is not classified as a dangerous good by the International Transport regulation.",
                      IndentedText))
        content.append(Spacer(1, 12))

        # Section 15
        content.append(Paragraph("15) Regulatory Information", styles['SectionHeader']))
        content.append(Paragraph(
            "This product is not classified in the list of controlled substances implemented by the government.",
            IndentedText))
        content.append(Spacer(1, 12))

        # Section 16
        content.append(Paragraph("16) Shelf-Life", styles['SectionHeader']))
        content.append(
            Paragraph("Twelve months from date of production when the product is stored in unbroken packaging.",
                      IndentedText))
        content.append(Spacer(1, 12))

        # Section 17
        content.append(Paragraph("17) Other Information", styles['SectionHeader']))
        content.append(Paragraph("None", IndentedText))
        content.append(PageBreak())

        doc.build(content)
        return filename

    def show_pdf_preview(self, filename: str):
        self.pdf_doc.load(filename)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def generate_and_preview(self):
        pdf_file = self.generate_pdf("test.pdf")
        self.show_pdf_preview(pdf_file)

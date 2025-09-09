
import platform

from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from db import db_con


class FileCOA(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Certificate of Analysis Preview")
        main_layout = QVBoxLayout(self)

        # PDF Document + Viewer
        self.pdf_doc = QPdfDocument(self)
        self.pdf_viewer = QPdfView(self)
        self.pdf_viewer.setDocument(self.pdf_doc)

        # Scrollable view with multiple pages
        self.pdf_viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

        dpi = 96
        letter_width = int(8.5 * dpi)  # 816 px
        self.pdf_viewer.setFixedWidth(letter_width)

        btn_download = QPushButton("Download")
        btn_print = QPushButton("Print")

        # Put them in a horizontal layout and center
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(btn_download)
        button_layout.addSpacing(20)  # space between buttons
        button_layout.addWidget(btn_print)
        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)
        # Center the viewer using a horizontal layout
        viewer_container = QHBoxLayout()
        viewer_container.addStretch(1)  # left stretch
        viewer_container.addWidget(self.pdf_viewer)
        viewer_container.addStretch(1)  # right stretch
        main_layout.addLayout(viewer_container)

    def generate_pdf(self, coa_id, filename):
        field_result = db_con.get_single_coa_data(coa_id)

        # Create PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(name="SectionHeader", fontSize=14, leading=14, spaceAfter=12, spaceBefore=6, bold=True))
        styles.add(ParagraphStyle(name="SubHeading", fontSize=12, leading=14, spaceAfter=4, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=14, spaceAfter=4))
        IndentedText = ParagraphStyle(
            'IndentedText',
            parent=styles['NormalText'],  # inherit font size, leading, etc.
            leftIndent=20  # indent in points
        )
        date_format = "%-d" if platform.system() != "Windows" else "%#d"
        content = []
        page_width = letter[0] - 50 - 50
        col_widths = [0.23 * page_width, 0.25 * page_width, 0.28 * page_width, 0.16 * page_width, 0.08 * page_width]
        content.append(Paragraph("Certificate of Analysis", styles['Title']))
        content.append(Spacer(1, 12))

        details = [
            ["Customer:", Paragraph(str(field_result[1]), styles['NormalText']), "", "", ""],
            ["Color Code:", Paragraph(str(field_result[2]), styles['NormalText']), "", "", ""],
            ["Quantity Deliver:", Paragraph(str(field_result[6]), styles['NormalText']), "", "", ""],
            ["Delivery Date:", Paragraph(str(field_result[7].strftime(f"%B {date_format}, %Y")), styles['NormalText']), "", "", ""],
            ["Lot Number:", Paragraph(str(field_result[3]), styles['NormalText']), "", "", ""],
            ["Production Date:", Paragraph(str(field_result[8].strftime(f"%B {date_format}, %Y")), styles['NormalText']), "", "", ""],
            ["Delivery receipt Number:", Paragraph(str(field_result[5]), styles['NormalText']), "", "P.O Number:", Paragraph(str(field_result[4]))],
        ]
        table = Table(details, colWidths=col_widths, spaceBefore=12, spaceAfter=12)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>Summary of Analysis</b>", styles["SubHeading"]))
        content.append(Spacer(1, 12))
        # Summary of Analysis Table
        db_con.get_coa_analysis_results(coa_id)
        rows = db_con.get_coa_analysis_results(coa_id)
        summary_data = [["", "Standard", "Delivery"]]
        for rows in rows:
            parameter = rows[0]
            standard_value = rows[1]
            delivery_value = rows[2]
            summary_data.append([parameter, standard_value, delivery_value])

        summary_table = Table(summary_data, colWidths=[180, 150, 150], hAlign="CENTER")
        summary_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        content.append(summary_table)
        content.append(Spacer(1, 20))

        name_len = len(field_result[10])
        lines = "_"
        for i in range(name_len):
            lines += "_"


        content.append(Paragraph("Certified by:", styles["NormalText"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph(lines, styles["NormalText"]))
        content.append(Paragraph(str(field_result[10]), styles["NormalText"]))
        content.append(Paragraph("Date: " + str(field_result[9].strftime(f"%B {date_format}, %Y")), styles["NormalText"]))
        content.append(Spacer(1, 20))

        # Storage section
        content.append(Paragraph("<b>Storage</b>", styles["NormalText"]))
        content.append(Paragraph(str(field_result[11]), IndentedText))
        content.append(Paragraph("<b>Shelf Life: </b>", styles["NormalText"]))
        content.append(Paragraph(str(field_result[11]), IndentedText))

        doc.build(content)
        return filename

    def show_pdf_preview(self, filename: str):
        self.pdf_doc.load(filename)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def generate_and_preview(self, coa_id, filename):
        filename = filename.upper()
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        pdf_file = self.generate_pdf(coa_id, filename)
        self.show_pdf_preview(pdf_file)


import platform
import io
from PyQt6.QtCore import QBuffer, QIODevice
from PyQt6.QtGui import QPainter
from PyQt6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from reportlab.lib.enums import TA_CENTER
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from alert import window_alert
from db import db_con
from print.pdf_header import add_first_page_header


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

        self.file_name = None
        self.coa_id = None

        btn_download = QPushButton("Download")
        btn_print = QPushButton("Print")
        btn_download.clicked.connect(lambda: self.download_pdf(self.coa_id, self.file_name))
        btn_print.clicked.connect(self.print_pdf)

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

    def generate_pdf(self, coa_id):
        field_result = db_con.get_single_coa_data(coa_id)

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50, leftMargin=50, topMargin=90, bottomMargin=50
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(name="SectionHeader", fontSize=14, leading=14, spaceAfter=12, spaceBefore=6, bold=True))
        styles.add(ParagraphStyle(name="SubHeading", fontSize=12, leading=14, spaceAfter=4, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=14, spaceAfter=4))
        IndentedText = ParagraphStyle('IndentedText', parent=styles['NormalText'], leftIndent=20)
        styles.add(ParagraphStyle(
            name="TitleSans",
            fontName="Helvetica-Bold",  # built-in font
            fontSize=32,
            leading=22,
            alignment=1,  # center
            spaceAfter=12
        ))
        date_format = "%-d" if platform.system() != "Windows" else "%#d"
        content = []
        page_width = letter[0] - 50 - 50
        col_widths = [0.23 * page_width, 0.25 * page_width, 0.28 * page_width, 0.16 * page_width, 0.08 * page_width]
        content.append(Paragraph("Certificate of Analysis", styles['TitleSans']))
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

        doc.build(content, onFirstPage=add_first_page_header)
        buffer.seek(0)
        return buffer.getvalue()  # returns PDF bytes

    def show_pdf_preview(self, coa_id, filename):
        self.file_name = filename
        self.coa_id = coa_id
        pdf_bytes = self.generate_pdf(coa_id)
        # Wrap the PDF bytes in a QBuffer
        self.buffer = QBuffer()  # keep it as an instance attribute so it's not garbage collected
        self.buffer.setData(pdf_bytes)
        self.buffer.open(QIODevice.OpenModeFlag.ReadOnly)

        # Load PDF from QBuffer
        self.pdf_doc.load(self.buffer)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def download_pdf(self, coa_id, filename):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            filename,  # default name
            "PDF Files (*.pdf)"
        )

        if not file_path:  # user cancelled
            return None

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        pdf_bytes = self.generate_pdf(coa_id)
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)

        window_alert.show_message(self, "Success", "File downloaded!", icon_type="info")

    def print_pdf(self):
        if not self.pdf_doc or self.pdf_doc.pageCount() == 0:
            return  # nothing to print

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("Print Certificate of Analysis")

        if dialog.exec():
            painter = QPainter(printer)
            render_opts = QPdfDocumentRenderOptions()

            for page_number in range(self.pdf_doc.pageCount()):
                if page_number > 0:
                    printer.newPage()

                target_rect = printer.pageRect(QPrinter.Unit.Point).toRectF()

                # Scale the page to fit the printer page
                self.pdf_doc.renderPage(
                    painter,
                    page_number,
                    target_rect,
                    render_opts
                )

            painter.end()

import platform
import io
from PyQt6.QtCore import QBuffer, QIODevice
from PyQt6.QtGui import QPainter
from PyQt6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from reportlab.lib.enums import TA_CENTER
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from alert import window_alert
from db import db_con
from print.pdf_header import add_first_page_header

class FileMSDS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material Safety Data Sheet Preview")
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
        self.msds_id = None

        btn_download = QPushButton("Download")
        btn_print = QPushButton("Print")
        btn_download.clicked.connect(lambda: self.download_pdf(self.msds_id, self.file_name))
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


    def generate_pdf(self, msds_id):
        field_result = db_con.get_single_msds_data(msds_id)

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
        styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=14, spaceAfter=4))
        IndentedText = ParagraphStyle(
            'IndentedText',
            parent=styles['NormalText'],  # inherit font size, leading, etc.
            leftIndent=40  # indent in points
        )
        styles.add(ParagraphStyle(
            name="TitleSans",
            fontName="Helvetica-Bold",  # built-in font
            fontSize=16,
            leading=22,
            spaceAfter=12
        ))
        content = []
        page_width = letter[0] - 50 - 50
        table_width = 0.90 * page_width
        col_widths = [0.3 * table_width, 0.05 * table_width, 0.65 * table_width]

        # Title
        content.append(Paragraph("TECHNICAL DATA AND MATERIAL SAFETY DATA SHEET", styles['TitleSans']))
        content.append(Spacer(1, 12))

        # Section 1
        content.append(Paragraph("1) Product Identification", styles['SectionHeader']))
        section1_content = [
            [Paragraph('Trade Name', styles['NormalText']), ':', Paragraph(str(field_result[1]), styles['NormalText'])],
            [Paragraph('Manufactured by', styles['NormalText']), ':', Paragraph(str(field_result[5]), styles['NormalText'])],
            [Paragraph('Tel No', styles['NormalText']), ':', Paragraph(str(field_result[6]), styles['NormalText'])],
            [Paragraph('Facsimile', styles['NormalText']), ':', Paragraph(str(field_result[7]), styles['NormalText'])],
            [Paragraph('Email Address', styles['NormalText']), ':', Paragraph(str(field_result[8]), styles['NormalText'])]
        ]

        # Create the table
        table = Table(section1_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)  # Adjust column widths as needed

        # Apply styles
        def table_style(table_design):
            return table_design.setStyle(TableStyle([
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
        content.append(Paragraph(str(field_result[9]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 3
        content.append(Paragraph("3) Hazard Information", styles['SectionHeader']))
        section3_content = [
            [Paragraph("• Preliminaries", styles['NormalText']), ":", Paragraph(str(field_result[10]), styles['NormalText'])],
            [Paragraph("• Preliminary route of entry", styles['NormalText']), ":", Paragraph(str(field_result[11]), styles['NormalText'])],
            [Paragraph("• Symptoms of exposure", styles['NormalText']), ":", Paragraph(str(field_result[12]), styles['NormalText'])],
            [Paragraph("• Restrictive conditions", styles['NormalText']), ":", Paragraph(str(field_result[13]), styles['NormalText'])],
            [Paragraph("• Eyes", styles['NormalText']), ":", Paragraph(str(field_result[14]), styles['NormalText'])]
        ]

        table = Table(section3_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(Paragraph("Adverse Human Health Effects", IndentedText))
        content.append(table)
        content.append(Spacer(1, 12))
        content.append(Paragraph(str(field_result[15]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 4
        content.append(Paragraph("4) First Aid Measures", styles['SectionHeader']))
        section4_content = [
            [Paragraph('• Inhalation', styles['NormalText']), ':', Paragraph(str(field_result[16]), styles['NormalText'])],
            [Paragraph('• Eyes', styles['NormalText']), ':', Paragraph(str(field_result[17]), styles['NormalText'])],
            [Paragraph('• Skin', styles['NormalText']), ':', Paragraph(str(field_result[18]),styles['NormalText'])],
            [Paragraph('• Ingestion', styles['NormalText']), ':', Paragraph(str(field_result[19]), styles['NormalText'])],
           ]

        # Create the table
        table = Table(section4_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 5
        content.append(Paragraph("5) Fire Fighting Measures", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[20]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 6
        content.append(Paragraph("6) Accidental Release Measures", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[21]),
                                 IndentedText))
        content.append(Spacer(1, 12))

        # Section 7
        content.append(Paragraph("7) Handling and Storage", styles['SectionHeader']))
        section7_content = [
            [Paragraph('• Handling', styles['NormalText']), ':', Paragraph(str(field_result[22]), styles['NormalText'])],
            [Paragraph('• Storage', styles['NormalText']), ':', Paragraph(str(field_result[23]), styles['NormalText'])]
        ]
        table = Table(section7_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 8
        content.append(Paragraph("8) Exposure Controls/ Personal Protection", styles['SectionHeader']))
        section8_content = [
            [Paragraph('Exposure Control', styles['NormalText']), ':', Paragraph(str(field_result[24]),styles['NormalText'])],
            [Paragraph('Respiratory Protection', styles['NormalText']), ':', Paragraph(str(field_result[25]), styles['NormalText'])],
            [Paragraph('Hand Protection', styles['NormalText']), ':', Paragraph(str(field_result[26]), styles['NormalText'])],
            [Paragraph('Eye Protection', styles['NormalText']), ':', Paragraph(str(field_result[27]), styles['NormalText'])],
            [Paragraph('Skin Protection', styles['NormalText']), ':', Paragraph(str(field_result[28]), styles['NormalText'])]
        ]
        table = Table(section8_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 9
        content.append(Paragraph("9) Physical & Chemical Properties", styles['SectionHeader']))
        section9_content = [
            [Paragraph('Appearance', styles['NormalText']), ':', Paragraph(str(field_result[29]), styles['NormalText'])],
            [Paragraph('Odor', styles['NormalText']), ':', Paragraph(str(field_result[30]), styles['NormalText'])],
            [Paragraph('Heat Stability (1-5)', styles['NormalText']), ':', Paragraph(str(field_result[31]), styles['NormalText'])],
            [Paragraph('Light fastness (1-8)', styles['NormalText']), ':', Paragraph(str(field_result[32]), styles['NormalText'])],
            [Paragraph('Decomposition (°C)', styles['NormalText']), ':', Paragraph(str(field_result[33]), styles['NormalText'])],
            [Paragraph('Flash Point (°C)', styles['NormalText']), ':', Paragraph(str(field_result[34]), styles['NormalText'])],
            [Paragraph('Auto Ignition (°C)', styles['NormalText']), ':', Paragraph(str(field_result[35]), styles['NormalText'])],
            [Paragraph('Explosion Property', styles['NormalText']), ':', Paragraph(str(field_result[36]), styles['NormalText'])],
            [Paragraph('Solubility (Water)', styles['NormalText']), ':', Paragraph(str(field_result[37]), styles['NormalText'])]
        ]

        # Create the table
        table = Table(section9_content, colWidths=col_widths, hAlign='RIGHT', spaceBefore=12)
        table_style(table)
        content.append(table)
        content.append(Spacer(1, 12))

        # Section 10
        content.append(Paragraph("10) Stability & Reactivity", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[38]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 11
        content.append(Paragraph("11) Toxicological Information", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[39]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 12
        content.append(Paragraph("12) Ecological Information", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[40]), IndentedText))
        content.append(Spacer(1, 12))
        # Section 13
        content.append(Paragraph("13) Disposal", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[41]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 14
        content.append(Paragraph("14) Transport Information", styles['SectionHeader']))
        content.append(
            Paragraph(str(field_result[42]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 15
        content.append(Paragraph("15) Regulatory Information", styles['SectionHeader']))
        content.append(Paragraph(
            str(field_result[43]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 16
        content.append(Paragraph("16) Shelf-Life", styles['SectionHeader']))
        content.append(
            Paragraph(str(field_result[44]), IndentedText))
        content.append(Spacer(1, 12))

        # Section 17
        content.append(Paragraph("17) Other Information", styles['SectionHeader']))
        content.append(Paragraph(str(field_result[45]), IndentedText))
        content.append(PageBreak())

        doc.build(content, onFirstPage=add_first_page_header)
        buffer.seek(0)
        return buffer.getvalue()  # returns PDF bytes

    def show_pdf_preview(self, msds_id, filename):
        self.file_name = filename
        self.msds_id = msds_id
        pdf_bytes = self.generate_pdf(msds_id)
        # Wrap the PDF bytes in a QBuffer
        self.buffer = QBuffer()  # keep it as an instance attribute so it's not garbage collected
        self.buffer.setData(pdf_bytes)
        self.buffer.open(QIODevice.OpenModeFlag.ReadOnly)

        # Load PDF from QBuffer
        self.pdf_doc.load(self.buffer)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def download_pdf(self, msds_id, filename):
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

        pdf_bytes = self.generate_pdf(msds_id)
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

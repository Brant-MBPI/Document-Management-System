import platform
import io
from PyQt6.QtCore import QBuffer, QIODevice, QSize, Qt, QPointF
from PyQt6.QtGui import QPainter, QPageSize, QPageLayout, QAction, QIcon
from PyQt6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from alert import window_alert
from db import db_con
from print.pdf_header import add_first_page_header, add_coa_header
from utils import abs_path


def split_by_comma(s):
    return [part.strip() for part in s.split(',')]


class FileTerumo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Certificate of Analysis Preview")
        self.setWindowIcon(QIcon(abs_path.resource("img/icon.ico")))
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

        btn_download.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;  /* Green */
                        color: white;
                        font-size: 14px;
                        font-weight: semi-bold;
                        padding: 8px 16px;
                        border: 1px solid #388E3C;
                        border-radius: 6px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #45A049;
                    }
                    QPushButton:pressed {
                        background-color: #397D3A;
                    }
                """)

        # Blue Print button
        btn_print.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;  /* Blue */
                        color: white;
                        font-size: 14px;
                        font-weight: semi-bold;
                        padding: 8px 16px;
                        border: 1px solid #1976D2;
                        border-radius: 6px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #1E88E5;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                """)

        main_layout.addLayout(button_layout)
        # Center the viewer using a horizontal layout
        viewer_container = QHBoxLayout()
        viewer_container.addStretch(1)  # left stretch
        viewer_container.addWidget(self.pdf_viewer)
        viewer_container.addStretch(1)  # right stretch
        main_layout.addLayout(viewer_container)

        self.print_action = QAction(self)
        self.print_action.setShortcut("Ctrl+P")
        self.print_action.triggered.connect(self.print_pdf)
        self.addAction(self.print_action)

    def generate_pdf(self, coa_id, is_rrf=False):
        field_result = db_con.get_single_coa_data(coa_id)
        terumo_res = db_con.get_single_terumo_data(coa_id)

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50, leftMargin=50, topMargin=90, bottomMargin=50
        )
        styles = getSampleStyleSheet()
        content = []
        # The add_coa_header function needs to be aware of whether it's Terumo or not
        # For now, let's assume it handles this based on the data it receives,
        # or we might need to pass an additional flag to it.
        # For this specific case, `add_first_page_header` is used which handles the general header.

        if terumo_res is not None:
            styles['Normal'].fontName = 'Helvetica'
            normal_style = styles['Normal']
            bold_style = ParagraphStyle('Bold', parent=normal_style, fontName='Helvetica-Bold')
            right_style = ParagraphStyle('Right', parent=normal_style, alignment=TA_RIGHT)
            center_style = ParagraphStyle('Center', parent=normal_style, alignment=TA_CENTER)
            left_style = ParagraphStyle('Left', parent=normal_style, alignment=TA_LEFT)
            title_style = ParagraphStyle('Title', parent=normal_style, fontName='Helvetica-Bold', fontSize=14,
                                         alignment=TA_CENTER)

            # --- Document Content Start ---

            # Certificate of Analysis Title
            content.append(Paragraph("<b>Certificate of Analysis</b>", title_style))
            content.append(Spacer(1, 24))

            # Delivery Date
            date_format = "%-d" if platform.system() != "Windows" else "%#d"
            delivery_date_str = field_result[7].strftime(f'%B {date_format}, %Y')
            content.append(Paragraph(f"Delivery Date: {delivery_date_str}", right_style))
            content.append(Spacer(1, 12))

            # Customer + Lot No.
            lot_no = f"{field_result[3]}"
            customer_data = [
                [Paragraph(f"<b>Customer Name:</b> {field_result[1]}", normal_style),
                 Paragraph(f"<b>Lot No.:</b> {lot_no}", normal_style)]
            ]
            customer_table = Table(customer_data, colWidths=[300, 212], hAlign='LEFT')
            customer_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
            content.append(customer_table)
            content.append(Spacer(1, 2))

            # Item Code + Quantity
            quantity = f"{field_result[6]}"
            item_data = [
                [Paragraph(f"<b>Item Code:</b> {terumo_res[2]}", normal_style),
                 Paragraph(f"<b>Quantity:</b> {quantity}", normal_style)],
                [Paragraph(f"<b>Item Description:</b> {str(terumo_res[3])}", normal_style),
                 Paragraph("", normal_style)]
            ]
            item_table = Table(item_data, colWidths=[300, 212], hAlign='LEFT')
            item_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            content.append(item_table)
            content.append(Spacer(1, 8))

            # --- Main Check Items Table ---
            diameter_parts = split_by_comma(str(terumo_res[7]))
            area_parts = split_by_comma(str(terumo_res[8]))
            count_parts = split_by_comma(str(terumo_res[9]))
            actual_parts = split_by_comma(str(terumo_res[10]))

            def get_padded_list(lst, size):
                return lst + [''] * (size - len(lst))

            diameter_parts = get_padded_list(diameter_parts, 2)
            area_parts = get_padded_list(area_parts, 2)
            count_parts = get_padded_list(count_parts, 2)
            actual_parts = get_padded_list(actual_parts, 2)

            appearance_std = "Free from foreign material. No stickiness of pellets"
            dimension_std = "3 x 3 ± 0.5 mm pellet diameter and length<br/>Single cut, partially cut or double pellet shall be treated as single pellet and must be within the set acceptance criteria"

            table_data = [
                [Paragraph('<b>Check items</b>', left_style),
                 Paragraph('<b>Standard</b>', center_style), '', '',
                 Paragraph('<b>Actual</b>', center_style),
                 Paragraph('<b>Judgement</b>', center_style)],

                [Paragraph('<b>Molded Chip Inspection</b>', left_style), '', '', '', '', ''],

                [Paragraph('Color', left_style),
                 Paragraph(str(terumo_res[4]), left_style), '', '',
                 Paragraph(str(terumo_res[5]), center_style),
                 Paragraph(str(terumo_res[6]), center_style)],

                [Paragraph('Foreign Material Contamination', left_style),
                 Paragraph('Diameter (mm)', center_style),
                 Paragraph('Area (mm²)', center_style),
                 Paragraph('Count', center_style), '',
                 Paragraph(str(terumo_res[11]), center_style)],

                ['', Paragraph(diameter_parts[0], center_style),
                 Paragraph(area_parts[0], center_style),
                 Paragraph(count_parts[0], center_style),
                 Paragraph(actual_parts[0], center_style), ''],

                ['', Paragraph(diameter_parts[1], center_style),
                 Paragraph(area_parts[1], center_style),
                 Paragraph(count_parts[1], center_style),
                 Paragraph(actual_parts[1], center_style), ''],

                [Paragraph('<b>Pellet Inspection</b>', left_style), '', '', '', '', ''],

                [Paragraph('Appearance', left_style),
                 Paragraph(appearance_std, left_style),
                 Paragraph('Start', center_style),
                 Paragraph('Middle', center_style),
                 Paragraph('End', center_style),
                 Paragraph(str(terumo_res[16]), center_style)],

                ['', '', Paragraph(str(terumo_res[13]), center_style),
                 Paragraph(str(terumo_res[14]), center_style),
                 Paragraph(str(terumo_res[15]), center_style), ''],

                [Paragraph('Dimension', left_style),
                 Paragraph(dimension_std, left_style),
                 Paragraph('Start', center_style),
                 Paragraph('Middle', center_style),
                 Paragraph('End', center_style),
                 Paragraph(str(terumo_res[21]), center_style)],

                ['', '', Paragraph(str(terumo_res[18]), center_style),
                 Paragraph(str(terumo_res[19]), center_style),
                 Paragraph(str(terumo_res[20]), center_style), ''],
            ]

            col_widths = [130, 90, 80, 80, 80, 80]

            main_table = Table(table_data, colWidths=col_widths, hAlign='CENTER')
            main_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                ('SPAN', (0, 1), (-1, 1)),  # Molded Chip Inspection
                ('SPAN', (0, 6), (-1, 6)),  # Pellet Inspection

                ('SPAN', (1, 2), (3, 2)),  # Color Standard
                ('SPAN', (0, 3), (0, 5)),  # Foreign Material Contamination
                ('SPAN', (5, 3), (5, 5)),  # Judgement FMC
                ('SPAN', (0, 7), (0, 8)),  # Appearance
                ('SPAN', (1, 7), (1, 8)),  # Appearance Standard
                ('SPAN', (5, 7), (5, 8)),  # Judgement Appearance
                ('SPAN', (0, 9), (0, 10)),  # Dimension
                ('SPAN', (1, 9), (1, 10)),  # Dimension Standard
                ('SPAN', (5, 9), (5, 10)),  # Judgement Dimension
            ]))
            content.append(main_table)
            content.append(Spacer(1, 18))

            # Remarks
            remarks_text = "Remarks: Attached are the same sample chips for the following number:"
            content.append(Paragraph(remarks_text, normal_style))

            # Put terumo_res[23] inside a table with a max width for wrapping
            remarks_table = Table(
                [[Paragraph(str(terumo_res[23]), normal_style)]],
                colWidths=[460]  # adjust width to fit your margins (letter is 612pt wide, margins 50 each → 512 usable)
            )
            remarks_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            content.append(remarks_table)

            content.append(Spacer(1, 36))

            # Approved by section
            # Approved by section (name inline and underlined, title below with indent)
            approved_by_html = f"<b>Approved by:</b> <u>{str(field_result[10])}</u>"
            content.append(Paragraph(approved_by_html, left_style))

            # Add position/title under the name with indentation
            position_html = f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{str(terumo_res[22])}"
            content.append(Paragraph(position_html, left_style))

            # --- Document Content End ---

        doc.build(content, onFirstPage=add_first_page_header)  # Use the correct header function
        buffer.seek(0)
        return buffer.getvalue()  # returns PDF bytes

    def show_pdf_preview(self, coa_id, filename, is_rrf):
        self.file_name = filename
        self.coa_id = coa_id
        pdf_bytes = self.generate_pdf(coa_id, is_rrf)
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
        try:
            if not self.pdf_doc or self.pdf_doc.pageCount() == 0:
                return  # nothing to print

            printer = QPrinter(QPrinter.PrinterMode.HighResolution)

            # Set printer page size using QPageLayout
            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.PageSizeId.Letter))
            printer.setPageLayout(page_layout)

            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Print Certificate of Analysis")

            if dialog.exec():
                painter = QPainter(printer)
                render_options = QPdfDocumentRenderOptions()

                # Choose a sufficiently high DPI for rendering the PDF to an image
                # 600 DPI is a good balance for print quality
                render_dpi = 600

                for i in range(self.pdf_doc.pageCount()):
                    if i > 0:
                        printer.newPage()

                    pdf_page_size_points = self.pdf_doc.pagePointSize(i)

                    render_dpi = 300
                    image_render_width_pixels = int(pdf_page_size_points.width() / 72.0 * render_dpi)
                    image_render_height_pixels = int(pdf_page_size_points.height() / 72.0 * render_dpi)

                    pdf_image = self.pdf_doc.render(
                        i,
                        QSize(image_render_width_pixels, image_render_height_pixels),
                        render_options
                    )

                    if not pdf_image.isNull():
                        # Use the full page, not the printable area
                        full_page_pixels = printer.paperRect(QPrinter.Unit.DevicePixel)

                        scaled_image = pdf_image.scaled(
                            full_page_pixels.size().toSize(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )

                        # Align to the top (no margin)
                        x = full_page_pixels.x() + (full_page_pixels.width() - scaled_image.width()) / 2
                        y = full_page_pixels.y()  # start at the very top

                        painter.drawImage(QPointF(x, y), scaled_image)
                painter.end()
        except Exception as e:
            print(f"An error occurred during printing: {e}")
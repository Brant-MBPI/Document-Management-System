from PyQt6.QtWidgets import QWidget
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class FileCOA(QWidget):
    def __init__(self, coa_id):
        super().__init__()
        self.coa_id = coa_id
        self.coa_data = self.get_coa_data(coa_id)
        self.init_ui()

    def get_coa_data(self, coa_id):
        # Fetch COA data from the database using the provided coa_id
        # This is a placeholder implementation; replace with actual DB call
        return {
            "customer_name": "Sample Customer",
            "color_code": "Red",
            "lot_number": "12345",
            "delivery_receipt_number": "67890",
            "delivery_date": "2024-01-01",
            "test_results": [
                {"test_name": "Test A", "result": "Pass"},
                {"test_name": "Test B", "result": "Fail"},
            ],
        }

    def init_ui(self):
        self.setWindowTitle("Certificate of Analysis")
        self.setGeometry(100, 100, 800, 600)
        self.generate_pdf()

    def generate_pdf(self):
        pdf_filename = f"COA_{self.coa_id}.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle(
            name="TitleStyle",
            parent=styles["Title"],
            fontSize=24,
            leading=28,
            alignment=1,
            spaceAfter=20,
        )
        elements.append(Paragraph("Certificate of Analysis", title_style))

        customer_info = f"""
        <b>Customer Name:</b> {self.coa_data['customer_name']}<br/>
        <b>Color Code:</b> {self.coa_data['color_code']}<br/>
        <b>Lot Number:</b> {self.coa_data['lot_number']}<br/>
        <b>Delivery Receipt Number:</b> {self.coa_data['delivery_receipt_number']}<br/>
        <b>Delivery Date:</b> {self.coa_data['delivery_date']}<br/>
        """
        elements.append(Paragraph(customer_info, styles["Normal"]))
        elements.append(Spacer(1, 12))

        table_data = [["Test Name", "Result"]]
        for test in self.coa_data["test_results"]:
            table_data.append([test["test_name"], test["result"]])

        table
from reportlab.lib import colors

from utils import abs_path


def add_first_page_header(canvas, doc):
    canvas.saveState()
    # Convert cm to points (1 cm ≈ 28.35 pt)
    cm = 28.35
    logo_width = 18.9 * cm
    logo_height = 3.14 * cm

    # Page size
    page_width, page_height = doc.pagesize

    logo_path = abs_path.resource("img/MBPI_Logo.jpg")

    # Center horizontally
    x = (page_width - logo_width) / 2
    y = page_height - logo_height  # topmost position

    # Draw logo with fixed size (ignore aspect ratio)
    canvas.drawImage(
        logo_path,
        x, y,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=False
    )

    canvas.setFont('Courier', 12)  # Use monospaced Courier font
    canvas.setFillColor(colors.dimgray)  # Set text color (optional, but good practice)

    form_id_text = "FM000034"
    # Calculate text width to precisely position it from the right edge
    text_width = canvas.stringWidth(form_id_text, 'Courier', 12)

    canvas.drawString(
        page_width - doc.rightMargin - text_width,
        doc.bottomMargin - 20,  # Adjust -20 to move it up or down from the bottom margin
        form_id_text
    )

    canvas.restoreState()

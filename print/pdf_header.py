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


def add_coa_header(canvas, doc):
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

    canvas.setFont('Times-Roman', 10)  # Times New Roman equivalent, size 10
    canvas.setFillColor(colors.dimgray)

    form_id_text = "FM000034"
    text_width = canvas.stringWidth(form_id_text, 'Times-Roman', 10)

    canvas.drawString(
        page_width - doc.rightMargin - text_width,
        doc.bottomMargin - 10,
        form_id_text
    )

    canvas.restoreState()


from utils import abs_path

from reportlab.lib import colors
from reportlab.lib.units import cm


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
    # cm = 28.35  # reportlab.lib.units already provides cm, so no need to redefine

    # Define dimensions based on the first logo
    logo_width = 18.9 * cm
    logo_height = 3.14 * cm

    # Page size
    page_width, page_height = doc.pagesize

    # --- First Logo (MBPI_Logo) ---
    logo_path = abs_path.resource("img/MBPI_Logo.jpg")

    # Center horizontally
    x_logo = (page_width - logo_width) / 2
    y_logo_top = page_height - logo_height  # topmost position for the first logo

    # Draw logo 1
    canvas.drawImage(
        logo_path,
        x_logo, y_logo_top,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=False # As per your original request for the first logo
    )

    # --- Second Image (coa_title.png) ---
    second_image_path = abs_path.resource("img/coa_title.png")
    second_image_width = logo_width
    second_image_height = logo_height

    x_second_image = x_logo
    y_second_image_top = y_logo_top - second_image_height + 0.5 * cm

    # Draw the second image
    try:
        canvas.drawImage(
            second_image_path,
            x_second_image, y_second_image_top,
            width=second_image_width,
            height=second_image_height,
            preserveAspectRatio=True  # Keeping preserveAspectRatio=True as it's generally good for titles
        )
    except Exception as e:
        print(f"Warning: Could not draw second image at {second_image_path}. Error: {e}")
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


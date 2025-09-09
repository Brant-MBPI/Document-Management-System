def add_first_page_header(canvas, doc):
    canvas.saveState()
    # Convert cm to points (1 cm ≈ 28.35 pt)
    cm = 28.35
    logo_width = 18.9 * cm
    logo_height = 3.14 * cm

    # Page size
    page_width, page_height = doc.pagesize

    logo_path = "img/MBPI_Logo.jpg"

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

    canvas.restoreState()

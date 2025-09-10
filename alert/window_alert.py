from PyQt6.QtWidgets import QMessageBox


def show_message(self, title, message, icon_type="info", is_confirmation=False):
    msg = QMessageBox(self)

    # Map icon_type string to QMessageBox.Icon
    icon_map = {
        "info": QMessageBox.Icon.Information,
        "warning": QMessageBox.Icon.Warning,
        "critical": QMessageBox.Icon.Critical,
        "question": QMessageBox.Icon.Question
    }
    msg.setIcon(icon_map.get(icon_type, QMessageBox.Icon.Information))

    msg.setWindowTitle(title)
    msg.setText(message)

    # If it's a confirmation dialog, set Yes/No buttons
    if is_confirmation:
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)  # Optional: default to No

    # Style the QMessageBox
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #fefefe;
            border-radius: 12px;
            font-size: 14px;
            font-family: Segoe UI, sans-serif;
        }
        QLabel {
            color: #333333;
            padding: 10px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 6px 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
    """)

    if is_confirmation:
        no_button = msg.button(QMessageBox.StandardButton.No)
        if no_button:  # Ensure button exists
            no_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336; /* Red */
                        color: white;
                        border-radius: 8px;
                        padding: 6px 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #e53935; }
                    QPushButton:pressed { background-color: #d32f2f; }
                """)

    result = msg.exec()

    # Return True if Yes, False if No
    if is_confirmation:
        return result == QMessageBox.StandardButton.Yes
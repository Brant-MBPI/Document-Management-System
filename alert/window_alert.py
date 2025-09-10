from PyQt6.QtWidgets import QMessageBox, QInputDialog, QPushButton, QDialogButtonBox


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


def show_text_input(self, title, label, default_text=""):
    input_dialog = QInputDialog(self)
    input_dialog.setWindowTitle(title)
    input_dialog.setLabelText(label)
    input_dialog.setTextValue(default_text)

    # Style the main dialog
    input_dialog.setStyleSheet("""
        QInputDialog {
            background-color: #fefefe;
            border-radius: 12px;
            font-size: 14px;
            font-family: Segoe UI, sans-serif;
        }
        QLabel {
            color: #333333;
            padding: 10px;
            font-size: 14px;
        }
        QLineEdit {
            font-size: 14px;
            padding: 6px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-bottom: 10px;
        }
    """)

    # Show the dialog non-modally first to create buttons
    input_dialog.show()
    input_dialog.repaint()  # Ensure UI is rendered

    button_box = input_dialog.findChild(QDialogButtonBox)
    if button_box:
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)

        if ok_button:
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; /* Green */
                    color: white;
                    border-radius: 8px;
                    padding: 6px 18px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #45a049; }
                QPushButton:pressed { background-color: #3e8e41; }
            """)
        if cancel_button:
            cancel_button.setStyleSheet("""
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

    result = input_dialog.exec()
    return input_dialog.textValue(), result == QInputDialog.DialogCode.Accepted
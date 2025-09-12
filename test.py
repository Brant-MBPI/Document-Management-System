import sys
from PyQt6.QtCore import QCoreApplication, QTimer

# Assuming your SyncDeliveryWorker class is in a file named 'sync_worker.py'
from db.db_dr import SyncDeliveryWorker

def handle_sync_result(success, message, extracted_data):
    """
    This function will be called when the SyncDeliveryWorker finishes its task.
    It now accepts a list of dictionaries with the specific fields requested.
    """
    print(f"--- Sync Finished! ---")
    print(f"Success: {success}")
    print(f"Message: {message}")

    if success:
        print("\n--- Displaying Extracted Delivery Data ---")
        if extracted_data:
            print(f"Found {len(extracted_data)} simplified data entries:")
            for i, entry in enumerate(extracted_data):
                print(f"\nEntry {i+1}:")
                print(f"  DR No: {entry.get('dr_no', 'N/A')}")
                print(f"  Delivery Date: {entry.get('delivery_date', 'N/A')}")
                print(f"  Customer Name: {entry.get('customer_name', 'N/A')}")
                print(f"  PO No: {entry.get('po_no', 'N/A')}")
                print(f"  Lot Numbers: {entry.get('lot_numbers', 'N/A')}")
                print(f"  Product Code: {entry.get('product_code', 'N/A')}")
                print("  --------------------")
        else:
            print("No simplified delivery data was extracted.")
    else:
        print("\n--- Sync Failed, no data to display from worker output. ---")


    QCoreApplication.quit() # Always quit the application when done

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)

    worker = SyncDeliveryWorker()
    # Connect the signal to the handler, matching the new signal signature
    worker.finished.connect(handle_sync_result)

    QTimer.singleShot(0, worker.run)

    sys.exit(app.exec())
import os
import sys
import traceback
import dbfread
from sqlalchemy import create_engine, text
from PyQt6.QtCore import QObject, pyqtSignal, QCoreApplication

# --- CONFIGURATION ---
DB_CONFIG = {
    "host": "192.168.1.13",
    "port": 5432,
    "dbname": "db_msds",
    "user": "postgres",
    "password": "mbpi"
}
DBF_BASE_PATH = r'\\system-server\SYSTEM-NEW-OLD'
DELIVERY_DBF_PATH = os.path.join(DBF_BASE_PATH, 'tbl_del01.dbf')
DELIVERY_ITEMS_DBF_PATH = os.path.join(DBF_BASE_PATH, 'tbl_del02.dbf')

# --- DATABASE ENGINE SETUP ---
db_url = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)
try:
    engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=3600)
except Exception as e:
    print(f"FATAL: Could not create database engine. Error: {e}")
    exit(1)


def create_delivery_legacy_tables():
    """Creates the necessary PostgreSQL tables for storing the legacy delivery data."""
    print("Initializing database tables for legacy delivery data...")
    try:
        with engine.connect() as connection:
            with connection.begin():
                # Primary table for delivery headers
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_delivery_primary (
                        id SERIAL PRIMARY KEY,
                        dr_no TEXT NOT NULL UNIQUE,
                        delivery_date DATE,
                        customer_name TEXT,
                        deliver_to TEXT,
                        address TEXT,
                        po_no TEXT,
                        order_form_no TEXT,
                        fg_out_id TEXT,
                        terms TEXT,
                        prepared_by TEXT,
                        encoded_by TEXT,
                        encoded_on TIMESTAMP,
                        edited_by TEXT,
                        edited_on TIMESTAMP,
                        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                        is_printed BOOLEAN NOT NULL DEFAULT FALSE
                    );
                """))

                # Items table for delivery details.
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_delivery_items (
                        id SERIAL PRIMARY KEY,
                        dr_no TEXT NOT NULL,
                        quantity NUMERIC(15, 6),
                        unit TEXT,
                        product_code TEXT,
                        product_color TEXT,
                        no_of_packing NUMERIC(15, 2),
                        weight_per_pack NUMERIC(15, 6),
                        lot_numbers TEXT,
                        attachments TEXT,
                        unit_price NUMERIC(15, 6),
                        lot_no_1 TEXT,
                        lot_no_2 TEXT,
                        lot_no_3 TEXT,
                        mfg_date TEXT,
                        alias_code TEXT,
                        alias_desc TEXT,
                        FOREIGN KEY (dr_no) REFERENCES product_delivery_primary (dr_no) ON DELETE CASCADE
                    );
                """))

        print("Database tables for delivery initialized successfully.")
    except Exception as e:
        print(f"FATAL: Could not initialize delivery database tables: {e}")
        raise


class SyncDeliveryWorker(QObject):
    """Syncs delivery data from legacy DBF files to PostgreSQL (incremental sync)."""
    finished = pyqtSignal(bool, str)

    def _get_safe_dr_num(self, dr_num_raw):
        if dr_num_raw is None:
            return None
        try:
            return str(int(float(dr_num_raw)))
        except (ValueError, TypeError):
            return None

    def _to_float(self, value, default=0.0):
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return float(str(value).strip()) if str(value).strip() else default
            except (ValueError, TypeError):
                return default

    def run(self):
        """Main execution method for the sync process (incremental)."""
        print("\n--- Starting Legacy Delivery Sync ---")
        try:
            # --- Step 0: Get last synced ID ---
            with engine.connect() as conn:
                last_id = conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM product_delivery_primary")).scalar()
            print(f"Last synced ID in PostgreSQL: {last_id}")

            # --- Step 1: Process Primary Delivery Headers (tbl_del01.dbf) ---
            primary_recs = []
            print(f"Step 1: Reading headers from '{os.path.basename(DELIVERY_DBF_PATH)}'")
            primary_count = 0

            with dbfread.DBF(DELIVERY_DBF_PATH, load=True, encoding='latin1') as dbf_primary:
                for r in dbf_primary:
                    primary_count += 1
                    dr_num = self._get_safe_dr_num(r.get('T_DRNUM'))
                    if not dr_num:
                        continue

                    # ✅ Only sync records newer than last synced ID
                    if primary_count <= last_id:
                        continue

                    address = (str(r.get('T_ADD1', '')).strip() + ' ' +
                               str(r.get('T_ADD2', '')).strip()).strip()

                    primary_recs.append({
                        "dr_no": dr_num,
                        "delivery_date": r.get('T_DRDATE'),
                        "customer_name": str(r.get('T_CUSTOMER', '')).strip(),
                        "deliver_to": str(r.get('T_DELTO', '')).strip(),
                        "address": address,
                        "po_no": str(r.get('T_CPONUM', '')).strip(),
                        "order_form_no": str(r.get('T_ORDERNUM', '')).strip(),
                        "terms": str(r.get('T_REMARKS', '')).strip(),
                        "prepared_by": str(r.get('T_USERID', '')).strip(),
                        "encoded_on": r.get('T_DENCODED'),
                        "is_deleted": bool(r.get('T_DELETED', False))
                    })

            print(f"-> Found {len(primary_recs)} new primary records to sync.")

            if not primary_recs:
                self.finished.emit(True, "Sync Info: No new delivery records found.")
                return

            # --- Step 2: Process Delivery Items (tbl_del02.dbf) ---
            new_dr_numbers = {rec['dr_no'] for rec in primary_recs}
            items_by_dr = {}
            item_count = 0
            print(f"Step 2: Reading items from '{os.path.basename(DELIVERY_ITEMS_DBF_PATH)}'")

            with dbfread.DBF(DELIVERY_ITEMS_DBF_PATH, load=True, encoding='latin1') as dbf_items:
                for item_rec in dbf_items:
                    dr_num = self._get_safe_dr_num(item_rec.get('T_DRNUM'))
                    if dr_num not in new_dr_numbers:
                        continue

                    item_count += 1
                    attachments = "\n".join(
                        filter(None, [str(item_rec.get(f'T_DESC{i}', '')).strip() for i in range(1, 5)]))

                    if dr_num not in items_by_dr:
                        items_by_dr[dr_num] = []
                    items_by_dr[dr_num].append({
                        "dr_no": dr_num,
                        "quantity": self._to_float(item_rec.get('T_TOTALWT')),
                        "unit": str(item_rec.get('T_TOTALWTU', '')).strip(),
                        "product_code": str(item_rec.get('T_PRODCODE', '')).strip(),
                        "product_color": str(item_rec.get('T_PRODCOLO', '')).strip(),
                        "no_of_packing": self._to_float(item_rec.get('T_NUMPACKI')),
                        "weight_per_pack": self._to_float(item_rec.get('T_WTPERPAC')),
                        "lot_numbers": "",
                        "attachments": attachments
                    })

            print(f"-> Found {item_count} new item records to sync.")

            # --- Step 3: Insert New Records ---
            print("Step 3: Writing new data to PostgreSQL...")
            with engine.connect() as conn:
                with conn.begin():
                    # Insert/Update headers
                    conn.execute(text("""
                        INSERT INTO product_delivery_primary (
                            dr_no, delivery_date, customer_name, deliver_to, address, po_no,
                            order_form_no, terms, prepared_by, encoded_on, is_deleted,
                            edited_by, edited_on, encoded_by
                        ) VALUES (
                            :dr_no, :delivery_date, :customer_name, :deliver_to, :address, :po_no,
                            :order_form_no, :terms, :prepared_by, :encoded_on, :is_deleted,
                            'DBF_SYNC', NOW(), :prepared_by
                        ) ON CONFLICT (dr_no) DO UPDATE SET
                            delivery_date = EXCLUDED.delivery_date,
                            customer_name = EXCLUDED.customer_name,
                            deliver_to = EXCLUDED.deliver_to,
                            address = EXCLUDED.address,
                            po_no = EXCLUDED.po_no,
                            order_form_no = EXCLUDED.order_form_no,
                            terms = EXCLUDED.terms,
                            prepared_by = EXCLUDED.prepared_by,
                            encoded_on = EXCLUDED.encoded_on,
                            is_deleted = EXCLUDED.is_deleted,
                            edited_by = 'DBF_SYNC',
                            edited_on = NOW()
                    """), primary_recs)

                    # Insert items
                    all_items_to_insert = [
                        item for dr_num in new_dr_numbers for item in items_by_dr.get(dr_num, [])
                    ]
                    if all_items_to_insert:
                        conn.execute(text("""
                            INSERT INTO product_delivery_items (
                                dr_no, quantity, unit, product_code, product_color,
                                no_of_packing, weight_per_pack, lot_numbers, attachments
                            ) VALUES (
                                :dr_no, :quantity, :unit, :product_code, :product_color,
                                :no_of_packing, :weight_per_pack, :lot_numbers, :attachments
                            )
                        """), all_items_to_insert)

            print("-> Database transaction committed successfully.")
            msg = (f"Delivery sync complete.\n"
                   f"{len(primary_recs)} new primary records and "
                   f"{item_count} new items processed.")
            self.finished.emit(True, msg)

        except dbfread.DBFNotFound as e:
            self.finished.emit(False, f"File Not Found: Missing DBF file.\nDetails: {e}")
        except Exception as e:
            trace_info = traceback.format_exc()
            print(f"DELIVERY SYNC ERROR: {e}\n{trace_info}")
            self.finished.emit(False, f"Unexpected error:\n{e}\n\nCheck logs for details.")


def handle_sync_finish(success, message):
    print("\n--- Sync Process Finished ---")
    print("Status:", "SUCCESS" if success else "FAILED")
    print("Message:", message)
    if QCoreApplication.instance():
        QCoreApplication.instance().quit()


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    print("--- Running Delivery Table Setup ---")
    create_delivery_legacy_tables()
    worker = SyncDeliveryWorker()
    worker.finished.connect(handle_sync_finish)
    worker.run()
    sys.exit()

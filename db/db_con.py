
import psycopg2

from db import db_dr


def get_connection():
    return psycopg2.connect(
        host="192.168.1.13",
        dbname="db_msds",
        user="postgres",
        password="mbpi",
        port="5432"
    )


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Material Safety Data Sheet
    cur.execute("""
        CREATE TABLE IF NOT EXISTS msds_sheets(
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100),
            trade_name VARCHAR(255) NOT NULL,
            product_code VARCHAR(100),
            creation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            last_modified_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

            manufacturer_info TEXT,
            contact_tel VARCHAR(50),
            contact_facsimile VARCHAR(50),
            contact_email VARCHAR(100),

            composition_info TEXT,

            hazard_preliminaries TEXT,
            hazard_entry_route TEXT,
            hazard_symptoms TEXT,
            hazard_restrictive_conditions TEXT,
            hazard_eyes TEXT,
            hazard_general_note TEXT,

            first_aid_inhalation TEXT,
            first_aid_eyes TEXT,
            first_aid_skin TEXT,
            first_aid_ingestion TEXT,

            fire_fighting_media TEXT,

            accidental_release_info TEXT,

            handling_info TEXT,
            storage_info TEXT,

            exposure_control_info TEXT,
            respiratory_protection TEXT,
            hand_protection TEXT,
            eye_protection TEXT,
            skin_protection TEXT,

            stability_reactivity TEXT,
            conditions_to_avoid TEXT,
            materials_to_avoid TEXT,
            hazardous_decomposition TEXT,
            toxicological_info TEXT,
            ecological_info TEXT,
            disposal_info TEXT,
            transport_info TEXT,
            regulatory_info TEXT,
            shelf_life_info TEXT,
            other_info TEXT
        );
    """)

    # section9
    cur.execute("""
            CREATE TABLE IF NOT EXISTS msds_section_9 (
                id SERIAL PRIMARY KEY,
                msds_id INTEGER NOT NULL REFERENCES msds_sheets(id) ON DELETE CASCADE,
                property_order INT NOT NULL, 
                property_name TEXT NOT NULL, 
                property_value TEXT
            );
        """)

    # Certificate of Analysis

    cur.execute("""
        CREATE TABLE IF NOT EXISTS certificates_of_analysis(
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255),
            color_code VARCHAR(100),
            
            lot_number VARCHAR(100) UNIQUE,
            po_number VARCHAR(100),
            delivery_receipt_number VARCHAR(100),
            quantity_delivered TEXT,
            delivery_date DATE,
            production_date DATE,
            certification_date DATE,
            certified_by VARCHAR(255),
            storage_instructions TEXT,
            shelf_life_coa VARCHAR(255),
            suitability TEXT,
            creation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_terumo (
            id SERIAL PRIMARY KEY,
            coa_id INTEGER NOT NULL REFERENCES certificates_of_analysis(id) ON DELETE CASCADE,
            item_code TEXT,
            item_description TEXT,
            color_std TEXT,
            color_actual TEXT,
            color_judgement VARCHAR(36),
            diameter_std TEXT,
            area_std TEXT,
            count_std TEXT,
            fmc_actual TEXT,
            fmc_judgement VARCHAR(36),
            appearance_std TEXT,
            appearance_start TEXT,
            appearance_mid TEXT,
            appearance_end TEXT,
            appearance_judgement VARCHAR(36),
            dimension_std TEXT,
            dimension_start TEXT,
            dimension_mid TEXT,
            dimension_end TEXT,
            dimension_judgement VARCHAR(36),
            approver_position TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS coa_analysis_results (
            id SERIAL PRIMARY KEY,
            coa_id INTEGER NOT NULL REFERENCES certificates_of_analysis(id) ON DELETE CASCADE,
            parameter_name VARCHAR(255) NOT NULL,
            standard_value VARCHAR(100),
            delivery_value VARCHAR(100)
        );
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS certificates_of_analysis_rrf(
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(255),
                color_code VARCHAR(100),

                lot_number VARCHAR(100) UNIQUE,
                po_number VARCHAR(100),
                rrf_number VARCHAR(100),
                quantity_delivered TEXT,
                delivery_date DATE,
                production_date DATE,
                certification_date DATE,
                certified_by VARCHAR(255),
                storage_instructions TEXT,
                shelf_life_coa VARCHAR(255),
                suitability TEXT,
                creation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS coa_analysis_results_rrf (
                id SERIAL PRIMARY KEY,
                coa_rrf_id INTEGER NOT NULL REFERENCES certificates_of_analysis_rrf(id) ON DELETE CASCADE,
                parameter_name VARCHAR(255) NOT NULL,
                standard_value VARCHAR(100),
                delivery_value VARCHAR(100)
            );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_user (
            id SERIAL PRIMARY KEY,
            username VARCHAR(128) NOT NULL,
            password VARCHAR(255)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_coa_certified_by (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        INSERT INTO tbl_coa_certified_by (name)
        SELECT t.name
        FROM (VALUES
            ('Marissa Naz'),
            ('Linzy Jam Bautista'),
            ('Geelyn Raeanne Rellin')
        ) AS t(name)
        WHERE NOT EXISTS (
            SELECT 1 FROM tbl_coa_certified_by
        );
    """)

    db_dr.create_delivery_legacy_tables()

    conn.commit()
    cur.close()
    conn.close()


# Create
def save_msds_sheet(data, section9):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Insert into msds_sheets
                cur.execute("""
                    INSERT INTO msds_sheets (
                        customer_name,
                        trade_name,
                        product_code,
                        manufacturer_info,
                        contact_tel,
                        contact_facsimile,
                        contact_email,
                        composition_info,
                        hazard_preliminaries,
                        hazard_entry_route,
                        hazard_symptoms,
                        hazard_restrictive_conditions,
                        hazard_eyes,
                        hazard_general_note,
                        first_aid_inhalation,
                        first_aid_eyes,
                        first_aid_skin,
                        first_aid_ingestion,
                        fire_fighting_media,
                        accidental_release_info,
                        handling_info,
                        storage_info,
                        exposure_control_info,
                        respiratory_protection,
                        hand_protection,
                        eye_protection,
                        skin_protection,
                        stability_reactivity,
                        conditions_to_avoid,
                        materials_to_avoid,
                        hazardous_decomposition,
                        toxicological_info,
                        ecological_info,
                        disposal_info,
                        transport_info,
                        regulatory_info,
                        shelf_life_info,
                        other_info
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id;
                """, (
                    data["customer_name"], data["trade_name"], data["product_code"], data["manufacturer_info"],
                    data["contact_tel"], data["contact_facsimile"], data["contact_email"], data["composition_info"],
                    data["hazard_preliminaries"], data["hazard_entry_route"], data["hazard_symptoms"],
                    data["hazard_restrictive_conditions"], data["hazard_eyes"], data["hazard_general_note"],
                    data["first_aid_inhalation"], data["first_aid_eyes"], data["first_aid_skin"],
                    data["first_aid_ingestion"], data["fire_fighting_media"], data["accidental_release_info"],
                    data["handling_info"], data["storage_info"], data["exposure_control_info"],
                    data["respiratory_protection"], data["hand_protection"], data["eye_protection"],
                    data["skin_protection"], data["stability_reactivity"], data["conditions_to_avoid"],
                    data["materials_to_avoid"], data["hazardous_decomposition"], data["toxicological_info"],
                    data["ecological_info"], data["disposal_info"], data["transport_info"],
                    data["regulatory_info"], data["shelf_life_info"], data["other_info"]
                ))
                msds_id = cur.fetchone()[0]

                # Insert Section 9 properties
                for idx, (property_name, property_value) in enumerate(section9.items(), start=1):
                    if property_name:
                        cur.execute("""
                            INSERT INTO msds_section_9 (msds_id, property_order, property_name, property_value)
                            VALUES (%s, %s, %s, %s)
                        """, (msds_id, idx, property_name, property_value))

    finally:
        if conn:
            conn.close()


def save_certificate_of_analysis(data, summary_of_analysis):
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert into certificates_of_analysis
        cur.execute("""
            INSERT INTO certificates_of_analysis (
                customer_name, 
                color_code, 
                lot_number, 
                po_number, 
                delivery_receipt_number, 
                quantity_delivered, 
                delivery_date, 
                production_date, 
                certification_date, 
                certified_by, 
                storage_instructions, 
                shelf_life_coa, 
                suitability
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data["customer_name"], data["color_code"], data["lot_number"], data["po_number"],
            data["delivery_receipt"], data["quantity_delivered"], data["delivery_date"],
            data["production_date"], data["creation_date"], data["certified_by"],
            data["storage"], data["shelf_life"], data["suitability"]
        ))

        coa_id = cur.fetchone()[0]

        # Insert analysis results
        for parameter, values in summary_of_analysis.items():
            standard_value = values[0]
            delivery_value = values[1]

            cur.execute("""
                INSERT INTO coa_analysis_results (
                    coa_id, parameter_name, standard_value, delivery_value
                ) VALUES (%s, %s, %s, %s)
            """, (coa_id, parameter, standard_value, delivery_value))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e


def save_terumo_coa(data, terumo):
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert into certificates_of_analysis
        cur.execute("""
            INSERT INTO certificates_of_analysis (
                customer_name, 
                color_code, 
                lot_number, 
                po_number, 
                delivery_receipt_number, 
                quantity_delivered, 
                delivery_date, 
                production_date, 
                certification_date, 
                certified_by, 
                storage_instructions, 
                shelf_life_coa, 
                suitability
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data["customer_name"], data["color_code"], data["lot_number"], data["po_number"],
            data["delivery_receipt"], data["quantity_delivered"], data["delivery_date"],
            data["production_date"], data["creation_date"], data["certified_by"],
            data["storage"], data["shelf_life"], data["suitability"]
        ))

        coa_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO tbl_terumo (
                coa_id,
                item_code, 
                item_description, 
                color_std, 
                color_actual, 
                color_judgement, 
                diameter_std, 
                area_std, 
                count_std, 
                fmc_actual, 
                fmc_judgement, 
                appearance_std, 
                appearance_start, 
                appearance_mid,
                appearance_end,
                appearance_judgement,
                dimension_std,
                dimension_start,
                dimension_mid,
                dimension_end,
                dimension_judgement,
                approver_position
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            coa_id, terumo["item_code"], terumo["item_description"], terumo["color_std"],
            terumo["color_actual"], terumo["color_judgement"], terumo["diameter_std"],
            terumo["area_std"], terumo["count_std"], terumo["fmc_actual"],
            terumo["fmc_judgement"], terumo["appearance_std"], terumo["appearance_start"],
            terumo["appearance_mid"], terumo["appearance_end"], terumo["appearance_judgement"],
            terumo["dimension_std"], terumo["dimension_start"], terumo["dimension_mid"],
            terumo["dimension_end"], terumo["dimension_judgement"], terumo["approver_position"]
        ))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def save_certificate_of_analysis_rrf(data, summary_of_analysis):
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert into certificates_of_analysis
        cur.execute("""
            INSERT INTO certificates_of_analysis_rrf (
                customer_name, 
                color_code, 
                lot_number, 
                po_number, 
                rrf_number, 
                quantity_delivered, 
                delivery_date, 
                production_date, 
                certification_date, 
                certified_by, 
                storage_instructions, 
                shelf_life_coa, 
                suitability
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data["customer_name"], data["color_code"], data["lot_number"], data["po_number"],
            data["delivery_receipt"], data["quantity_delivered"], data["delivery_date"],
            data["production_date"], data["creation_date"], data["certified_by"],
            data["storage"], data["shelf_life"], data["suitability"]
        ))

        coa_rrf_id = cur.fetchone()[0]

        # Insert analysis results
        for parameter, values in summary_of_analysis.items():
            standard_value = values[0]
            delivery_value = values[1]

            cur.execute("""
                INSERT INTO coa_analysis_results_rrf (
                    coa_rrf_id, parameter_name, standard_value, delivery_value
                ) VALUES (%s, %s, %s, %s)
            """, (coa_rrf_id, parameter, standard_value, delivery_value))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e


# Update
def update_msds_sheet(msds_id, data, section9):
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Update main MSDS sheet
                cur.execute("""
                    UPDATE msds_sheets
                    SET 
                        customer_name = %s,
                        trade_name = %s,
                        product_code = %s,
                        manufacturer_info = %s,
                        contact_tel = %s,
                        contact_facsimile = %s,
                        contact_email = %s,
                        composition_info = %s,
                        hazard_preliminaries = %s,
                        hazard_entry_route = %s,
                        hazard_symptoms = %s,
                        hazard_restrictive_conditions = %s,
                        hazard_eyes = %s,
                        hazard_general_note = %s,
                        first_aid_inhalation = %s,
                        first_aid_eyes = %s,
                        first_aid_skin = %s,
                        first_aid_ingestion = %s,
                        fire_fighting_media = %s,
                        accidental_release_info = %s,
                        handling_info = %s,
                        storage_info = %s,
                        exposure_control_info = %s,
                        respiratory_protection = %s,
                        hand_protection = %s,
                        eye_protection = %s,
                        skin_protection = %s,
                        stability_reactivity = %s,
                        conditions_to_avoid = %s,
                        materials_to_avoid = %s,
                        hazardous_decomposition = %s,
                        toxicological_info = %s,
                        ecological_info = %s,
                        disposal_info = %s,
                        transport_info = %s,
                        regulatory_info = %s,
                        shelf_life_info = %s,
                        other_info = %s,
                        last_modified_date = NOW()
                    WHERE id = %s;
                """, (
                    data["customer_name"], data["trade_name"], data["product_code"], data["manufacturer_info"],
                    data["contact_tel"], data["contact_facsimile"], data["contact_email"], data["composition_info"],
                    data["hazard_preliminaries"], data["hazard_entry_route"], data["hazard_symptoms"],
                    data["hazard_restrictive_conditions"], data["hazard_eyes"], data["hazard_general_note"],
                    data["first_aid_inhalation"], data["first_aid_eyes"], data["first_aid_skin"],
                    data["first_aid_ingestion"], data["fire_fighting_media"], data["accidental_release_info"],
                    data["handling_info"], data["storage_info"], data["exposure_control_info"],
                    data["respiratory_protection"], data["hand_protection"], data["eye_protection"],
                    data["skin_protection"], data["stability_reactivity"], data["conditions_to_avoid"],
                    data["materials_to_avoid"], data["hazardous_decomposition"], data["toxicological_info"],
                    data["ecological_info"], data["disposal_info"], data["transport_info"],
                    data["regulatory_info"], data["shelf_life_info"], data["other_info"],
                    msds_id
                ))

                # --- Section 9 update ---
                # Clear old Section 9 records
                cur.execute("DELETE FROM msds_section_9 WHERE msds_id = %s", (msds_id,))

                # Insert fresh Section 9 records
                for idx, (property_name, property_value) in enumerate(section9.items(), start=1):
                    if property_name:
                        cur.execute("""
                            INSERT INTO msds_section_9 (msds_id, property_order, property_name, property_value)
                            VALUES (%s, %s, %s, %s)
                        """, (msds_id, idx, property_name, property_value))

    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def update_certificate_of_analysis(coa_id, data, summary_of_analysis):
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert into certificates_of_analysis
        cur.execute("""
            UPDATE certificates_of_analysis
            SET 
                customer_name = %s, 
                color_code = %s, 
                lot_number = %s, 
                po_number = %s, 
                delivery_receipt_number = %s, 
                quantity_delivered = %s, 
                delivery_date = %s, 
                production_date = %s, 
                certification_date = %s, 
                certified_by = %s, 
                storage_instructions = %s, 
                shelf_life_coa = %s, 
                suitability = %s
            WHERE id = %s;
        """, (
            data["customer_name"], data["color_code"], data["lot_number"], data["po_number"],
            data["delivery_receipt"], data["quantity_delivered"], data["delivery_date"],
            data["production_date"], data["creation_date"], data["certified_by"],
            data["storage"], data["shelf_life"], data["suitability"],
            coa_id
        ))
        # Delete existing analysis results
        cur.execute("""
            DELETE FROM coa_analysis_results WHERE coa_id = %s;
        """, (coa_id,))

        # Insert analysis results
        for parameter, values in summary_of_analysis.items():
            standard_value = values[0]
            delivery_value = values[1]

            cur.execute("""
                INSERT INTO coa_analysis_results (
                    coa_id, parameter_name, standard_value, delivery_value
                ) VALUES (%s, %s, %s, %s)
            """, (coa_id, parameter, standard_value, delivery_value))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e


def update_certificate_of_analysis_rrf(coa_id, data, summary_of_analysis):
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert into certificates_of_analysis
        cur.execute("""
            UPDATE certificates_of_analysis_rrf
            SET 
                customer_name = %s, 
                color_code = %s, 
                lot_number = %s, 
                po_number = %s, 
                rrf_number = %s, 
                quantity_delivered = %s, 
                delivery_date = %s, 
                production_date = %s, 
                certification_date = %s, 
                certified_by = %s, 
                storage_instructions = %s, 
                shelf_life_coa = %s, 
                suitability = %s
            WHERE id = %s;
        """, (
            data["customer_name"], data["color_code"], data["lot_number"], data["po_number"],
            data["delivery_receipt"], data["quantity_delivered"], data["delivery_date"],
            data["production_date"], data["creation_date"], data["certified_by"],
            data["storage"], data["shelf_life"], data["suitability"],
            coa_id
        ))
        # Delete existing analysis results
        cur.execute("""
            DELETE FROM coa_analysis_results_rrf WHERE coa_rrf_id = %s;
        """, (coa_id,))

        # Insert analysis results
        for parameter, values in summary_of_analysis.items():
            standard_value = values[0]
            delivery_value = values[1]

            cur.execute("""
                INSERT INTO coa_analysis_results_rrf (
                    coa_rrf_id, parameter_name, standard_value, delivery_value
                ) VALUES (%s, %s, %s, %s)
            """, (coa_id, parameter, standard_value, delivery_value))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e


#     Read
def get_all_msds_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM msds_sheets ORDER BY id DESC;")
    records = cur.fetchall()

    cur.close()
    conn.close()
    return records


def get_all_coa_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM certificates_of_analysis ORDER BY id DESC;")
    records = cur.fetchall()

    cur.close()
    conn.close()
    return records


def get_all_coa_data_rrf():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM certificates_of_analysis_rrf ORDER BY id DESC;")
    records = cur.fetchall()

    cur.close()
    conn.close()
    return records


def get_single_msds_data(msds_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM msds_sheets WHERE id = %s;",
        (msds_id,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    return record


def get_trade_name_msds(code):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT trade_name FROM msds_sheets WHERE product_code = %s;",
        (code,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_single_msds_section9(msds_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM msds_section_9 WHERE msds_id = %s ORDER BY property_order ASC;",
        (msds_id,)
    )
    record = cur.fetchall()  # only one row expected

    cur.close()
    conn.close()
    return record


def get_single_coa_data(coa_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM certificates_of_analysis WHERE id = %s;",
        (coa_id,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    return record


def get_coa_analysis_results(coa_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT parameter_name, standard_value, delivery_value 
        FROM coa_analysis_results 
        WHERE coa_id = %s;
    """, (coa_id,))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results


def get_single_coa_data_rrf(coa_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM certificates_of_analysis_rrf WHERE id = %s;",
        (coa_id,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    return record


def get_coa_analysis_results_rrf(coa_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT parameter_name, standard_value, delivery_value 
        FROM coa_analysis_results_rrf 
        WHERE coa_rrf_id = %s;
    """, (coa_id,))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results


# Delete
def delete_msds_sheet(msds_id):
    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM msds_sheets WHERE id = %s;", (msds_id,))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e


def delete_certificate_of_analysis(coa_id):
    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM certificates_of_analysis WHERE id = %s;", (coa_id,))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e


def delete_certificate_of_analysis_rrf(coa_id):
    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM certificates_of_analysis_rrf WHERE id = %s;", (coa_id,))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e


def get_dr_details(dr_no):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT a.dr_no, a.product_code, b.customer_name, b.delivery_date, b.po_no, a.attachments, 
                    TO_CHAR(a.quantity, 'FM999999990.00') || ' ' || a.unit AS quantity
                    FROM product_delivery_items a, product_delivery_primary b
                    WHERE a.dr_no = b.dr_no AND a.dr_no=%s ORDER BY a.id DESC""",
        (dr_no,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_rrf_details(rrf_no):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT a.rrf_no, a.product_code, b.customer_name, b.rrf_date, a.remarks, 
                    TO_CHAR(a.quantity, 'FM999999990.00') || ' ' || a.unit AS quantity
                    FROM rrf_items a, rrf_primary b
                    WHERE a.rrf_no = b.rrf_no AND a.rrf_no=%s ORDER BY a.id DESC""",
        (rrf_no,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_rrf_lot_po(dr_no):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT b.po_no, a.attachments
                    FROM product_delivery_items a, product_delivery_primary b
                    WHERE a.dr_no = b.dr_no AND a.dr_no=%s ORDER BY a.id DESC""",
        (dr_no,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_rrf_prod_date(dr_no):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT production_date FROM certificates_of_analysis
                    WHERE delivery_receipt_number=%s;""",
        (dr_no,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_summary_from_msds(code, dr_no):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT 
                    a.id,
                    i.product_color
                FROM msds_sheets a
                JOIN product_delivery_items i 
                    ON a.product_code = i.product_code
                JOIN product_delivery_primary p 
                    ON i.dr_no = p.dr_no
                WHERE a.product_code = %s
                  AND i.dr_no = %s
                ORDER BY a.id DESC LIMIT 1;
            """,
        (code, dr_no,)
    )
    record = cur.fetchone()  # only one row expected

    cur.close()
    conn.close()
    if record is None:
        return ()  # or return None, depending on how you want to handle it
    return record


def get_all_dr_no():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT dr_no FROM product_delivery_items ORDER BY CAST(dr_no AS INTEGER);")
    records = cur.fetchall()  # only one row expected

    cur.close()
    conn.close()
    return [row[0] for row in records]


def get_all_rrf_no():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT rrf_no FROM rrf_items ORDER BY CAST(rrf_no AS INTEGER);")
    records = cur.fetchall()  # only one row expected

    cur.close()
    conn.close()
    return [row[0] for row in records]


def get_all_certified_by():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM tbl_coa_certified_by;")
    records = cur.fetchall()  # only one row expected

    cur.close()
    conn.close()
    return [row[0] for row in records]


def get_coa_table_msds(msds_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT property_value
        FROM msds_section_9 
        WHERE msds_id = %s 
          AND property_name IN ('Heat Stability (1-5)', 'Light fastness (1-8)')
        ORDER BY CASE property_name
            WHEN 'Light fastness (1-8)' THEN 1
            WHEN 'Heat Stability (1-5)' THEN 2 END;
    """, (msds_id,))
    results = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()
    return results


def authenticate_user(username, hashed_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM tbl_user WHERE username = %s AND password = %s",
        (username, hashed_password)
    )
    return cur.fetchone()


def register_user(username, hashed_password):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e

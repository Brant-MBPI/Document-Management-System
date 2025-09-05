
import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="password",
        port="5433"
    )


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Material Safety Data Sheet
    cur.execute("""
        CREATE TABLE IF NOT EXISTS msds_sheets(
            id SERIAL PRIMARY KEY,
            trade_name VARCHAR(255) NOT NULL,
            product_code VARCHAR(100) UNIQUE,
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
            
            appearance VARCHAR(100),
            odor VARCHAR(100),
            heat_stability VARCHAR(50),
            light_fastness VARCHAR(50),
            decomposition_temp VARCHAR(50),
            flash_point VARCHAR(50),
            auto_ignition_temp VARCHAR(50),
            explosion_property VARCHAR(50),
            solubility_water VARCHAR(100),
            
            stability_reactivity TEXT,
            toxicological_info TEXT,
            ecological_info TEXT,
            disposal_info TEXT,
            transport_info TEXT,
            regulatory_info TEXT,
            shelf_life_info TEXT,
            other_info TEXT
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
            quantity_delivered NUMERIC(10, 2),
            delivery_date DATE,
            production_date DATE,
            certification_date DATE,
            certified_by VARCHAR(255),
            storage_instructions TEXT,
            shelf_life_coa VARCHAR(100),
            suitability TEXT,
            creation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
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
        CREATE TABLE IF NOT EXISTS tbl_user (
            id SERIAL PRIMARY KEY,
            username VARCHAR(128) NOT NULL,
            password VARCHAR(255)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# Create
def save_msds_sheet(data):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO msds_sheets (
                trade_name,
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
                appearance,
                odor,
                heat_stability,
                light_fastness,
                decomposition_temp,
                flash_point,
                auto_ignition_temp,
                explosion_property,
                solubility_water,
                stability_reactivity,
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
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s
            )
            RETURNING id;
        """, (
            data["trade_name"], data["manufacturer_info"], data["contact_tel"],
            data["contact_facsimile"], data["contact_email"], data["composition_info"],
            data["hazard_preliminaries"], data["hazard_entry_route"], data["hazard_symptoms"],
            data["hazard_restrictive_conditions"], data["hazard_eyes"], data["hazard_general_note"],
            data["first_aid_inhalation"], data["first_aid_eyes"], data["first_aid_skin"],
            data["first_aid_ingestion"], data["fire_fighting_media"], data["accidental_release_info"],
            data["handling_info"], data["storage_info"], data["exposure_control_info"],
            data["respiratory_protection"], data["hand_protection"], data["eye_protection"],
            data["skin_protection"], data["appearance"], data["odor"],
            data["heat_stability"], data["light_fastness"], data["decomposition_temp"],
            data["flash_point"], data["auto_ignition_temp"], data["explosion_property"],
            data["solubility_water"], data["stability_reactivity"], data["toxicological_info"],
            data["ecological_info"], data["disposal_info"], data["transport_info"],
            data["regulatory_info"], data["shelf_life_info"], data["other_info"]
        ))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e


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


#     Read

def get_all_coa_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM certificates_of_analysis;")
    records = cur.fetchall()

    cur.close()
    conn.close()
    return records


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

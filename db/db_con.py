
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
import psycopg2
import psycopg2.extras

DB_CONFIG = {
    'dbname': 'cbt_system',
    'user': 'postgres',
    'password': 'yourpassword',
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    # Run schema manually via schema.sql
    pass

def get_exams():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM exams ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def create_user(first_name, last_name, email, role, password_hash, biometric_template, biometric_type):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (first_name, last_name, email, role, password_hash, biometric_template, biometric_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id
            """, 
            (first_name, last_name, email, role, password_hash, biometric_template, biometric_type)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print("Error creating user:", e)
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

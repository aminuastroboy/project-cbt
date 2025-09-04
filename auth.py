import psycopg2, psycopg2.extras, hashlib
from db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(first, last, email, password, role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (first_name, last_name, email, password_hash, role, biometric_template)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, 
            (first, last, email, hash_password(password), role, b'FAKE_BIOMETRIC')
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error registering user:", e)
        return False
    finally:
        cur.close()
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE email=%s AND password_hash=%s",
                (email, hash_password(password)))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

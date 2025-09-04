# db.py — Database access helpers (PostgreSQL)
import psycopg2, psycopg2.extras
from typing import Dict, Any

DB_CONFIG = {
    "dbname": "cbt_system",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": "5432",
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        role VARCHAR(20) CHECK (role IN ('student','admin','invigilator')) NOT NULL,
        password_hash TEXT NOT NULL,
        biometric_template BYTEA,
        biometric_type VARCHAR(20) DEFAULT 'face',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS exams (
        exam_id SERIAL PRIMARY KEY,
        exam_name VARCHAR(200) NOT NULL,
        created_by INT REFERENCES users(user_id) ON DELETE SET NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS questions (
        question_id SERIAL PRIMARY KEY,
        exam_id INT REFERENCES exams(exam_id) ON DELETE CASCADE,
        question_text TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option CHAR(1) CHECK (correct_option IN ('A','B','C','D')) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS results (
        result_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        exam_id INT REFERENCES exams(exam_id) ON DELETE CASCADE,
        score INT NOT NULL,
        taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS answers (
        answer_id SERIAL PRIMARY KEY,
        result_id INT REFERENCES results(result_id) ON DELETE CASCADE,
        question_id INT REFERENCES questions(question_id) ON DELETE CASCADE,
        selected_option CHAR(1) CHECK (selected_option IN ('A','B','C','D')) NOT NULL
    );
    "
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(ddl)
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None

def email_exists(email: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE email=%s", (email,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

def save_user(first_name, last_name, email, role, password_hash, face_encoding, biometric_type="face"):
    conn = get_connection()
    cur = conn.cursor()
    bt = face_encoding.tobytes() if face_encoding is not None else None
    cur.execute("""
        INSERT INTO users (first_name,last_name,email,role,password_hash,biometric_template,biometric_type)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (first_name, last_name, email, role, password_hash, bt, biometric_type))
    conn.commit()
    cur.close()
    conn.close()

def create_exam(exam_name: str, creator_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO exams (exam_name, created_by) VALUES (%s,%s) RETURNING exam_id",
                (exam_name, creator_id))
    exam_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return exam_id

def get_exams():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM exams ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]

def add_question(exam_id, q_text, a, b, c, d, correct):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questions (exam_id, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (exam_id, q_text, a, b, c, d, correct))
    conn.commit()
    cur.close()
    conn.close()

def get_questions(exam_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM questions WHERE exam_id=%s ORDER BY question_id ASC", (exam_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]

def save_result(user_id, exam_id, answers_dict):
    qs = get_questions(exam_id)
    qmap = {q["question_id"]: q for q in qs}
    correct = 0
    for qid, ans in answers_dict.items():
        if qid in qmap and ans == qmap[qid]["correct_option"]:
            correct += 1
    score = int((correct / len(qs)) * 100) if qs else 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (user_id, exam_id, score) VALUES (%s,%s,%s) RETURNING result_id",
                (user_id, exam_id, score))
    result_id = cur.fetchone()[0]
    for qid, ans in answers_dict.items():
        cur.execute("INSERT INTO answers (result_id, question_id, selected_option) VALUES (%s,%s,%s)",
                    (result_id, qid, ans))
    conn.commit()
    cur.close()
    conn.close()
    return score

def get_results_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT r.score, r.taken_at, e.exam_name
        FROM results r
        JOIN exams e ON e.exam_id = r.exam_id
        WHERE r.user_id=%s
        ORDER BY r.taken_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]

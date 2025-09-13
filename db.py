import psycopg2
import psycopg2.extras

DB_NAME = "cbt_system"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_conn():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(open("schema.sql", "r").read())
    conn.commit()
    conn.close()

def add_user(username, password, role, face_encoding):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role, face_encoding) VALUES (%s, %s, %s, %s)", 
                (username, password, role, face_encoding))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    conn.close()
    return user

def add_exam(name, examiner_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO exams (name, examiner_id) VALUES (%s, %s)", (name, examiner_id))
    conn.commit()
    conn.close()

def get_exams():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exams")
    exams = cur.fetchall()
    conn.close()
    return exams

def add_question(exam_id, question, opt_a, opt_b, opt_c, opt_d, correct):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions (exam_id, question, opt_a, opt_b, opt_c, opt_d, correct) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                (exam_id, question, opt_a, opt_b, opt_c, opt_d, correct))
    conn.commit()
    conn.close()

def get_questions(exam_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE exam_id=%s", (exam_id,))
    questions = cur.fetchall()
    conn.close()
    return questions

def save_result(student_id, exam_id, score):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (student_id, exam_id, score) VALUES (%s, %s, %s)", 
                (student_id, exam_id, score))
    conn.commit()
    conn.close()

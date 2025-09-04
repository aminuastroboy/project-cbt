-- schema.sql — CBT with Biometric Verification (PostgreSQL)
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
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_results_user ON results(user_id);
CREATE INDEX IF NOT EXISTS idx_results_exam ON results(exam_id);

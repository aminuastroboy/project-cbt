-- Database schema for CBT System with Biometrics
-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('student','admin','invigilator')),
    biometric_template BYTEA,
    biometric_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exams table
CREATE TABLE IF NOT EXISTS exams (
    exam_id SERIAL PRIMARY KEY,
    exam_name VARCHAR(200) NOT NULL,
    course_code VARCHAR(20),
    duration_minutes INT,
    created_by INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
CREATE TABLE IF NOT EXISTS questions (
    question_id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(exam_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option CHAR(1) CHECK (correct_option IN ('A','B','C','D'))
);

-- Results table
CREATE TABLE IF NOT EXISTS results (
    result_id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(exam_id),
    student_id INT REFERENCES users(user_id),
    score INT,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

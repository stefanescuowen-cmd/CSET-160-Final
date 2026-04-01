-- Reset root password and flush privileges
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Stevens2023!';
FLUSH PRIVILEGES;

-- Drop database if it exists (start fresh)
DROP DATABASE IF EXISTS exam_platform;

-- Create database
CREATE DATABASE exam_platform;
USE exam_platform;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    role ENUM('student', 'teacher'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tests table
CREATE TABLE tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    teacher_id INT,
    is_timed BOOLEAN DEFAULT FALSE,
    duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- Questions table
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    question_text TEXT,
    type ENUM('open') DEFAULT 'open',
    FOREIGN KEY (test_id) REFERENCES tests(id)
);

-- Submissions table
CREATE TABLE submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    student_id INT,
    marks INT,
    graded_by INT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_late BOOLEAN DEFAULT FALSE,
    UNIQUE (test_id, student_id),
    FOREIGN KEY (test_id) REFERENCES tests(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (graded_by) REFERENCES users(id)
);

-- Answers table
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT,
    question_id INT,
    answer_text TEXT,
    FOREIGN KEY (submission_id) REFERENCES submissions(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
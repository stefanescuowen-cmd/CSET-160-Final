ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Stevens2023!';
FLUSH PRIVILEGES;

CREATE DATABASE exam_platform;

-- Users
create table users(
id int auto_increment primary key,
name varchar(100),
email varchar(100),
role enum ('student', 'teacher'),
created_at timestamp default current_timestamp
);

-- Tests
CREATE TABLE tests(
id int auto_increment primary key,
title varchar(255),
teacher_id int,
is_timed boolean default false,
duration int,
created_at timestamp default current_timestamp,
foreign key (teacher_id) references users(id)
);

-- Questions
create table questions(
id int auto_increment primary key,
test_id int,
question_text TEXT,
type enum('open', 'mcq'),
foreign key (test_id) references tests(id)
);

-- MCQ Options
create table options(
id int auto_increment primary key,
question_id int,
option_text text,
foreign key (question_id) references questions(id)
);

-- Submissions
create table submissions(
id int auto_increment primary key,
test_id int,
student_id int,
marks int,
graded_by int,
submitted_at timestamp default current_timestamp,
is_late boolean default false,
unique (test_id, student_id),
foreign key (test_id) references tests(id),
foreign key (student_id) references users(id),
foreign key (graded_by) references users(id)
);

-- Answers
create table answers(
id int auto_increment primary key,
submission_id int,
question_id int,
answer_text text,
foreign key (submission_id) references submissions(id),
foreign key (question_id) references questions(id)
);
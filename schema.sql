DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS Results;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    lastname TEXT
    );

CREATE TABLE quiz (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    qz_subject TEXT,
    questions INTEGER,
    quiz_date DATE
    );

CREATE TABLE results (
    results_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER
   );

INSERT INTO students (student_id, firstname, lastname) VALUES (1, 'John', 'Smith');
INSERT INTO quiz (quiz_id, qz_subject, questions, quiz_date) VALUES (1, 'Python Basics', 5, '2015-05-05');
INSERT INTO results (score, quiz_id, student_id) VALUES (85, 1, 1);
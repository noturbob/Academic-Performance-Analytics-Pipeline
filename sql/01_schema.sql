-- ACADEMIC PERFORMANCE DATABASE SCHEMA

DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS performance CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- STUDENTS TABLE
CREATE TABLE students (
    hall_ticket VARCHAR(20) PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    program VARCHAR(100)
);

-- SUBJECTS TABLE
CREATE TABLE subjects (
    course_code VARCHAR(20) PRIMARY KEY,
    course_title VARCHAR(200) NOT NULL,
    credits INT NOT NULL
);

-- PERFORMANCE TABLE
CREATE TABLE performance (
    hall_ticket VARCHAR(20) REFERENCES students(hall_ticket),
    semester VARCHAR(20),
    sgpa DECIMAL(4,2),
    result VARCHAR(20),
    total_subjects INT,
    performance_category VARCHAR(20),
    avg_grade_points DECIMAL(4,2),
    min_grade_points INT,
    max_grade_points INT,
    std_grade_points DECIMAL(4,2),
    fail_count INT,
    PRIMARY KEY (hall_ticket, semester)
);

-- GRADES TABLE
CREATE TABLE grades (
    hall_ticket VARCHAR(20) REFERENCES students(hall_ticket),
    course_code VARCHAR(20) REFERENCES subjects(course_code),
    grade VARCHAR(2) NOT NULL,
    grade_points INT,
    result VARCHAR(10),
    credits INT,
    semester VARCHAR(20),
    PRIMARY KEY (hall_ticket, course_code, semester)
);

-- CREATE INDEXES
CREATE INDEX idx_grades_hall_ticket ON grades(hall_ticket);
CREATE INDEX idx_grades_course ON grades(course_code);
CREATE INDEX idx_grades_grade ON grades(grade);
CREATE INDEX idx_performance_sgpa ON performance(sgpa);
CREATE INDEX idx_performance_category ON performance(performance_category);
-- ACADEMIC PERFORMANCE ANALYSIS QUERIES

-- QUERY 1: OVERALL CLASS STATISTICS
SELECT 
    COUNT(*) as total_students,
    ROUND(AVG(sgpa), 2) as avg_sgpa,
    ROUND(MIN(sgpa), 2) as min_sgpa,
    ROUND(MAX(sgpa), 2) as max_sgpa,
    ROUND(AVG(CASE WHEN sgpa IS NOT NULL THEN (sgpa - (SELECT AVG(sgpa) FROM performance WHERE sgpa IS NOT NULL)) * (sgpa - (SELECT AVG(sgpa) FROM performance WHERE sgpa IS NOT NULL)) ELSE 0 END), 2) as variance_sgpa,
    SUM(CASE WHEN result = 'PASS' THEN 1 ELSE 0 END) as passed_students,
    SUM(CASE WHEN result = 'PROMOTED' THEN 1 ELSE 0 END) as promoted_students,
    ROUND(100.0 * SUM(CASE WHEN result = 'PASS' THEN 1 ELSE 0 END) / COUNT(*), 2) as pass_percentage
FROM performance
WHERE sgpa IS NOT NULL;

-- QUERY 2: PERFORMANCE CATEGORY DISTRIBUTION
SELECT 
    performance_category,
    COUNT(*) as student_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    ROUND(AVG(sgpa), 2) as avg_sgpa,
    ROUND(MIN(sgpa), 2) as min_sgpa,
    ROUND(MAX(sgpa), 2) as max_sgpa
FROM performance
GROUP BY performance_category
ORDER BY 
    CASE performance_category
        WHEN 'Distinction' THEN 1
        WHEN 'First Class' THEN 2
        WHEN 'Second Class' THEN 3
        WHEN 'Pass Class' THEN 4
        WHEN 'At Risk' THEN 5
        ELSE 6
    END;

-- QUERY 3: TOP 10 STUDENTS
SELECT 
    s.student_name,
    s.hall_ticket,
    p.sgpa,
    p.performance_category,
    p.fail_count
FROM performance p
JOIN students s ON p.hall_ticket = s.hall_ticket
WHERE p.sgpa IS NOT NULL
ORDER BY p.sgpa DESC
LIMIT 10;

-- QUERY 4: STUDENTS AT RISK (Low SGPA or Fails)
SELECT 
    s.student_name,
    s.hall_ticket,
    p.sgpa,
    p.fail_count,
    p.performance_category
FROM performance p
JOIN students s ON p.hall_ticket = s.hall_ticket
WHERE p.sgpa < 7 OR p.fail_count > 0
ORDER BY p.sgpa;

-- QUERY 5: GRADE DISTRIBUTION
SELECT 
    grade,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM grades
GROUP BY grade
ORDER BY 
    CASE grade
        WHEN 'O' THEN 1
        WHEN 'A+' THEN 2
        WHEN 'A' THEN 3
        WHEN 'B+' THEN 4
        WHEN 'B' THEN 5
        WHEN 'C' THEN 6
        WHEN 'D' THEN 7
        WHEN 'F' THEN 8
    END;

-- QUERY 6: SUBJECT PERFORMANCE ANALYSIS
SELECT 
    sub.course_code,
    sub.course_title,
    COUNT(g.hall_ticket) as total_enrolled,
    SUM(CASE WHEN g.result = 'PASS' THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN g.result = 'FAIL' THEN 1 ELSE 0 END) as failed,
    ROUND(100.0 * SUM(CASE WHEN g.result = 'PASS' THEN 1 ELSE 0 END) / COUNT(*), 2) as pass_rate,
    ROUND(AVG(g.grade_points), 2) as avg_grade_points
FROM grades g
JOIN subjects sub ON g.course_code = sub.course_code
GROUP BY sub.course_code, sub.course_title
ORDER BY pass_rate;

-- QUERY 7: HARDEST SUBJECTS (by fail rate)
SELECT 
    sub.course_code,
    sub.course_title,
    COUNT(g.hall_ticket) as total_enrolled,
    SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) as fail_count,
    ROUND(100.0 * SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) / COUNT(*), 2) as fail_rate,
    ROUND(AVG(g.grade_points), 2) as avg_grade_points
FROM grades g
JOIN subjects sub ON g.course_code = sub.course_code
GROUP BY sub.course_code, sub.course_title
HAVING fail_count > 0
ORDER BY fail_rate DESC;

-- QUERY 8: EASIEST SUBJECTS (highest avg grade points)
SELECT 
    sub.course_code,
    sub.course_title,
    COUNT(g.hall_ticket) as total_enrolled,
    ROUND(AVG(g.grade_points), 2) as avg_grade_points,
    SUM(CASE WHEN g.grade IN ('O', 'A+') THEN 1 ELSE 0 END) as excellent_count,
    ROUND(100.0 * SUM(CASE WHEN g.grade IN ('O', 'A+') THEN 1 ELSE 0 END) / COUNT(*), 2) as excellence_rate
FROM grades g
JOIN subjects sub ON g.course_code = sub.course_code
GROUP BY sub.course_code, sub.course_title
ORDER BY avg_grade_points DESC;

-- QUERY 9: GRADE DISTRIBUTION BY SUBJECT
SELECT 
    sub.course_title,
    SUM(CASE WHEN g.grade = 'O' THEN 1 ELSE 0 END) as O_count,
    SUM(CASE WHEN g.grade = 'A+' THEN 1 ELSE 0 END) as A_plus_count,
    SUM(CASE WHEN g.grade = 'A' THEN 1 ELSE 0 END) as A_count,
    SUM(CASE WHEN g.grade = 'B+' THEN 1 ELSE 0 END) as B_plus_count,
    SUM(CASE WHEN g.grade = 'B' THEN 1 ELSE 0 END) as B_count,
    SUM(CASE WHEN g.grade = 'C' THEN 1 ELSE 0 END) as C_count,
    SUM(CASE WHEN g.grade = 'D' THEN 1 ELSE 0 END) as D_count,
    SUM(CASE WHEN g.grade = 'F' THEN 1 ELSE 0 END) as F_count
FROM grades g
JOIN subjects sub ON g.course_code = sub.course_code
GROUP BY sub.course_title;

-- QUERY 10: STUDENTS WITH PERFECT SCORES
SELECT 
    s.student_name,
    s.hall_ticket,
    COUNT(g.grade) as total_subjects,
    SUM(CASE WHEN g.grade = 'O' THEN 1 ELSE 0 END) as O_grades,
    p.sgpa
FROM grades g
JOIN students s ON g.hall_ticket = s.hall_ticket
JOIN performance p ON s.hall_ticket = p.hall_ticket
GROUP BY s.student_name, s.hall_ticket, p.sgpa
HAVING SUM(CASE WHEN g.grade = 'O' THEN 1 ELSE 0 END) >= 3
ORDER BY p.sgpa DESC;

-- QUERY 11: CORRELATION BETWEEN SGPA AND GRADE CONSISTENCY
SELECT 
    p.performance_category,
    ROUND(AVG(p.sgpa), 2) as avg_sgpa,
    ROUND(AVG(p.std_grade_points), 2) as avg_std_deviation,
    COUNT(*) as student_count
FROM performance p
WHERE p.sgpa IS NOT NULL AND p.std_grade_points IS NOT NULL
GROUP BY p.performance_category
ORDER BY avg_sgpa DESC;

-- QUERY 12: SUBJECT-WISE PERCENTILE ANALYSIS
WITH subject_percentiles AS (
    SELECT 
        course_code,
        grade_points,
        NTILE(4) OVER (PARTITION BY course_code ORDER BY grade_points) as quartile
    FROM grades
    WHERE grade_points IS NOT NULL
)
SELECT 
    sub.course_title,
    MIN(CASE WHEN sp.quartile = 1 THEN sp.grade_points END) as Q1_25th_percentile,
    MIN(CASE WHEN sp.quartile = 2 THEN sp.grade_points END) as Q2_median,
    MIN(CASE WHEN sp.quartile = 3 THEN sp.grade_points END) as Q3_75th_percentile,
    MAX(sp.grade_points) as max_grade_points
FROM subject_percentiles sp
JOIN subjects sub ON sp.course_code = sub.course_code
GROUP BY sub.course_title;
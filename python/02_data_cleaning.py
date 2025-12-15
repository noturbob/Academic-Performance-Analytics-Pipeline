import pandas as pd
import json
import numpy as np
import os

print("Starting data cleaning and transformation...\n")

# Create output directories
os.makedirs('data/cleaned', exist_ok=True)
os.makedirs('docs/reports', exist_ok=True)

# Load JSON
with open('data/raw data/batch_student_data.json', 'r') as f:
    raw_data = json.load(f)

# 1. CREATE STUDENTS TABLE
students = []
for record in raw_data:
    student = record['student']
    students.append({
        'hall_ticket': student['hallTicket'],
        'student_name': student['name'],
        'father_name': student['fatherName'],
        'mother_name': student['motherName'],
        'program': student['program']
    })

students_df = pd.DataFrame(students)
students_df = students_df.drop_duplicates(subset=['hall_ticket'])

print(f"Students table: {len(students_df)} students")

# 2. CREATE SUBJECTS TABLE
subjects_set = set()
for record in raw_data:
    for subject in record['semesters'][0]['subjects']:
        subjects_set.add((
            subject['courseCode'],
            subject['courseTitle'],
            subject['credits']
        ))

subjects_df = pd.DataFrame(list(subjects_set), 
                           columns=['course_code', 'course_title', 'credits'])
subjects_df = subjects_df.sort_values('course_code')

print(f"Subjects table: {len(subjects_df)} subjects")

# 3. CREATE GRADES TABLE
grades_data = []
for record in raw_data:
    student = record['student']
    semester_info = record['semesters'][0]
    
    for subject in semester_info['subjects']:
        grades_data.append({
            'hall_ticket': student['hallTicket'],
            'course_code': subject['courseCode'],
            'grade': subject['grade'],
            'result': subject['result'],
            'credits': subject['credits'],
            'semester': 'SEMESTER-V'
        })

grades_df = pd.DataFrame(grades_data)

print(f"Grades table: {len(grades_df)} grade records")

# 4. CREATE PERFORMANCE TABLE
performance_data = []
for record in raw_data:
    student = record['student']
    semester_info = record['semesters'][0]
    
    sgpa = semester_info['sgpa']
    
    performance_data.append({
        'hall_ticket': student['hallTicket'],
        'semester': 'SEMESTER-V',
        'sgpa': float(sgpa) if sgpa else None,
        'result': semester_info['result'],
        'total_subjects': record['totalSubjects']
    })

performance_df = pd.DataFrame(performance_data)

print(f"Performance table: {len(performance_df)} records")

# 5. ADD GRADE POINT CONVERSION
grade_points = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'B': 6,
    'C': 5,
    'D': 4,
    'F': 0
}

grades_df['grade_points'] = grades_df['grade'].map(grade_points)
grades_df['grade_points'] = grades_df['grade_points'].fillna(0).astype(int)

# 6. CALCULATE SUBJECT PERFORMANCE
subject_performance = grades_df.groupby('course_code').agg({
    'result': lambda x: (x == 'PASS').sum(),
    'grade': 'count',
    'grade_points': 'mean'
}).reset_index()

subject_performance.columns = ['course_code', 'passed', 'total_enrolled', 'avg_grade_points']
subject_performance['pass_rate'] = (subject_performance['passed'] / subject_performance['total_enrolled'] * 100).round(2)
subject_performance['fail_count'] = subject_performance['total_enrolled'] - subject_performance['passed']

# Merge with subject names
subject_performance = subject_performance.merge(subjects_df[['course_code', 'course_title']], on='course_code')

# 7. STUDENT PERFORMANCE CATEGORIES
def categorize_sgpa(sgpa):
    if pd.isna(sgpa):
        return 'Promoted'
    elif sgpa >= 9:
        return 'Distinction'
    elif sgpa >= 8:
        return 'First Class'
    elif sgpa >= 7:
        return 'Second Class'
    elif sgpa >= 6:
        return 'Pass Class'
    else:
        return 'At Risk'

performance_df['performance_category'] = performance_df['sgpa'].apply(categorize_sgpa)

# 8. CALCULATE STUDENT-LEVEL AGGREGATES
student_aggregates = grades_df.groupby('hall_ticket').agg({
    'grade_points': ['mean', 'min', 'max', 'std'],
    'grade': lambda x: (x == 'F').sum()
}).reset_index()

student_aggregates.columns = ['hall_ticket', 'avg_grade_points', 'min_grade_points', 
                               'max_grade_points', 'std_grade_points', 'fail_count']

# Merge with performance data
performance_df = performance_df.merge(student_aggregates, on='hall_ticket', how='left')

# 9. SAVE CLEANED DATA
students_df.to_csv('data/cleaned/students.csv', index=False)
subjects_df.to_csv('data/cleaned/subjects.csv', index=False)
grades_df.to_csv('data/cleaned/grades.csv', index=False)
performance_df.to_csv('data/cleaned/performance.csv', index=False)
subject_performance.to_csv('data/cleaned/subject_performance.csv', index=False)

print(f"\nAll tables saved to data/cleaned/")

# 10. DATA QUALITY REPORT
report = f"""
{'='*60}
DATA CLEANING REPORT - SEMESTER V
{'='*60}

TABLES CREATED:
--------------
1. Students: {len(students_df)} students
2. Subjects: {len(subjects_df)} subjects  
3. Grades: {len(grades_df)} grade records
4. Performance: {len(performance_df)} performance records
5. Subject Performance: {len(subject_performance)} subject statistics

PERFORMANCE DISTRIBUTION:
------------------------
{performance_df['performance_category'].value_counts().to_string()}

PASS/FAIL SUMMARY:
-----------------
{performance_df['result'].value_counts().to_string()}

SGPA STATISTICS:
---------------
Mean: {performance_df['sgpa'].mean():.2f}
Median: {performance_df['sgpa'].median():.2f}
Std Dev: {performance_df['sgpa'].std():.2f}
Min: {performance_df['sgpa'].min():.2f}
Max: {performance_df['sgpa'].max():.2f}

SUBJECT DIFFICULTY (by pass rate):
----------------------------------
{subject_performance.nsmallest(5, 'pass_rate')[['course_code', 'course_title', 'pass_rate', 'fail_count']].to_string(index=False)}

GRADE DISTRIBUTION:
------------------
{grades_df['grade'].value_counts().to_string()}

DATA QUALITY:
------------
Missing SGPA values: {performance_df['sgpa'].isna().sum()}
Total grade records: {len(grades_df)}
Fail grades: {(grades_df['grade'] == 'F').sum()}
Pass rate: {(grades_df['result'] == 'PASS').sum() / len(grades_df) * 100:.2f}%

{'='*60}
"""

with open('docs/reports/cleaning_report.txt', 'w') as f:
    f.write(report)

print("\nReport saved to: docs/reports/cleaning_report.txt")
print("\nDATA CLEANING COMPLETE!")
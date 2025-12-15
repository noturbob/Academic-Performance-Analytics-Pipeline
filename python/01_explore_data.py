import pandas as pd
import json
import numpy as np

print("="*60)
print("SEMESTER 5 ACADEMIC PERFORMANCE - DATA EXPLORATION")
print("="*60)

# Load JSON data
with open('data/raw data/batch_student_data.json', 'r') as f:
    data = json.load(f)

print(f"\nTotal Records: {len(data)}")

# Convert to DataFrame for analysis
students_data = []

for record in data:
    student = record['student']
    semester_info = record['semesters'][0]
    
    student_row = {
        'name': student['name'],
        'hall_ticket': student['hallTicket'],
        'program': student['program'],
        'semester': semester_info['semester'],
        'sgpa': float(semester_info['sgpa']) if semester_info['sgpa'] else None,
        'result': semester_info['result'],
        'total_subjects': record['totalSubjects']
    }
    
    # Add subject-wise grades
    for subject in semester_info['subjects']:
        subject_code = subject['courseCode']
        student_row[f"{subject_code}_grade"] = subject['grade']
        student_row[f"{subject_code}_credits"] = subject['credits']
    
    students_data.append(student_row)

df = pd.DataFrame(students_data)

print(f"\nDataset Shape: {df.shape}")
print(f"Students: {len(df)}")
print(f"Columns: {len(df.columns)}")

# SGPA Statistics
sgpa_clean = df['sgpa'].dropna()
print(f"\nSGPA STATISTICS:")
print(f"Mean SGPA: {sgpa_clean.mean():.2f}")
print(f"Median SGPA: {sgpa_clean.median():.2f}")
print(f"Min SGPA: {sgpa_clean.min():.2f}")
print(f"Max SGPA: {sgpa_clean.max():.2f}")
print(f"Std Dev: {sgpa_clean.std():.2f}")
print(f"Students with SGPA: {len(sgpa_clean)}")
print(f"Students without SGPA (Promoted): {df['sgpa'].isna().sum()}")

# Result Distribution
print(f"\nRESULT DISTRIBUTION:")
print(df['result'].value_counts())

# Grade Distribution
all_grades = []
for col in df.columns:
    if '_grade' in col:
        all_grades.extend(df[col].tolist())

grade_counts = pd.Series(all_grades).value_counts()
print(f"\nOVERALL GRADE DISTRIBUTION:")
print(grade_counts)
print(f"\nTotal Grades: {len(all_grades)}")
print(f"Pass Grades (O, A+, A, B+, B, C, D): {sum(grade_counts[grade_counts.index != 'F'])}")
print(f"Fail Grades (F): {grade_counts.get('F', 0)}")

# Subjects taken
print(f"\nSUBJECTS IN SEMESTER 5:")
grade_cols = [col for col in df.columns if '_grade' in col]
subject_codes = set()
for col in grade_cols:
    subject_code = col.replace('_grade', '')
    subject_codes.add(subject_code)

print(f"Total unique subjects: {len(subject_codes)}")
for subject in sorted(subject_codes):
    print(f"  - {subject}")

# Performance categories
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

df['performance_category'] = df['sgpa'].apply(categorize_sgpa)

print(f"\nPERFORMANCE CATEGORIES:")
print(df['performance_category'].value_counts())

print("\nExploration Complete!")
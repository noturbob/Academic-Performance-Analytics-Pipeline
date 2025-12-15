import pandas as pd
from sqlalchemy import create_engine
import time

print("Loading data to SQL database...\n")

# Create SQLite connection
engine = create_engine('sqlite:///data/academic_performance.db')

# Load cleaned data
students = pd.read_csv('data/cleaned/students.csv')
subjects = pd.read_csv('data/cleaned/subjects.csv')
grades = pd.read_csv('data/cleaned/grades.csv')
performance = pd.read_csv('data/cleaned/performance.csv')

print(f"Loaded datasets:")
print(f"   Students: {len(students)} rows")
print(f"   Subjects: {len(subjects)} rows")
print(f"   Grades: {len(grades)} rows")
print(f"   Performance: {len(performance)} rows")

# Load to database
print(f"\nLoading to SQLite database...")

start_time = time.time()

students.to_sql('students', engine, if_exists='replace', index=False)
subjects.to_sql('subjects', engine, if_exists='replace', index=False)
grades.to_sql('grades', engine, if_exists='replace', index=False)
performance.to_sql('performance', engine, if_exists='replace', index=False)

elapsed = time.time() - start_time

print(f"Loaded in {elapsed:.2f} seconds")

# Verify
print(f"\nVerifying database...")

from sqlalchemy import text
with engine.connect() as conn:
    for table in ['students', 'subjects', 'grades', 'performance']:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.fetchone()[0]
        print(f"   {table}: {count} rows")

print(f"\nDatabase created: data/academic_performance.db")
print(f"Loading complete!")
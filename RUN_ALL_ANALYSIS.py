"""
MASTER SCRIPT: COMPLETE ACADEMIC PERFORMANCE ANALYSIS
======================================================
Semester V Results Analysis Pipeline
Executes all analysis steps from data exploration to ML predictions
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Create necessary directories
os.makedirs('data/cleaned', exist_ok=True)
os.makedirs('data/exports', exist_ok=True)
os.makedirs('docs/reports', exist_ok=True)
os.makedirs('python/outputs', exist_ok=True)
os.makedirs('r/outputs', exist_ok=True)
os.makedirs('ml_models', exist_ok=True)

print("\n" + "="*80)
print(" "*20 + "ACADEMIC PERFORMANCE ANALYSIS PIPELINE")
print(" "*25 + "SEMESTER V - 2025")
print("="*80 + "\n")

# Define all steps
steps = [
    {
        'name': 'Data Exploration',
        'script': 'python/01_explore_data.py',
        'description': 'Initial data exploration and summary statistics'
    },
    {
        'name': 'Data Cleaning & Transformation',
        'script': 'python/02_data_cleaning.py',
        'description': 'Clean data, create tables, calculate aggregates'
    },
    {
        'name': 'Load to Database',
        'script': 'python/03_load_to_sql.py',
        'description': 'Load cleaned data into SQLite database'
    },
    {
        'name': 'SQL Analysis Queries',
        'script': 'python/04_run_sql_queries.py',
        'description': 'Execute SQL analysis queries and export results'
    },
    {
        'name': 'Python Visualizations',
        'script': 'python/05_visualizations.py',
        'description': 'Generate matplotlib/seaborn visualizations'
    },
    {
        'name': 'Machine Learning Models',
        'script': 'python/06_ml_models.py',
        'description': 'Build SGPA prediction and at-risk classification models'
    },
    {
        'name': 'R Statistical Analysis',
        'script': 'r/01_statistical_analysis.R',
        'description': 'Perform comprehensive statistical analysis in R'
    }
]

# Track results
results = {
    'completed': [],
    'failed': [],
    'skipped': []
}

def run_python_script(script_path):
    """Execute Python script"""
    try:
        import sys
        # Use the current Python interpreter
        subprocess.run([sys.executable, script_path], check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"Script not found: {script_path}")
        return False

def run_r_script(script_path):
    """Execute R script"""
    try:
        subprocess.run(['Rscript', script_path], check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"R not found in PATH. Skipping R analysis.")
        return False

# Execute all steps
for i, step in enumerate(steps, 1):
    print(f"\n{'-'*80}")
    print(f"STEP {i}/{len(steps)}: {step['name'].upper()}")
    print(f"{'-'*80}")
    print(f"Description: {step['description']}")
    print(f"Script: {step['script']}")
    print()
    
    if not os.path.exists(step['script']):
        print(f"⚠️  Script not found: {step['script']}")
        results['skipped'].append(step['name'])
        continue
    
    start_time = time.time()
    print(f"Starting at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Execute based on script type
    if step['script'].endswith('.py'):
        success = run_python_script(step['script'])
    elif step['script'].endswith('.R'):
        success = run_r_script(step['script'])
    else:
        success = False
    
    elapsed_time = time.time() - start_time
    
    if success:
        print(f"\n✓ COMPLETED in {elapsed_time:.2f} seconds")
        results['completed'].append(step['name'])
    else:
        print(f"\n✗ FAILED (took {elapsed_time:.2f} seconds)")
        results['failed'].append(step['name'])

# Generate summary report
print("\n\n" + "="*80)
print(" "*25 + "PIPELINE EXECUTION SUMMARY")
print("="*80 + "\n")

print(f"Completed Steps: {len(results['completed'])}/{len(steps)}")
for step in results['completed']:
    print(f"  ✓ {step}")

if results['failed']:
    print(f"\nFailed Steps: {len(results['failed'])}")
    for step in results['failed']:
        print(f"  ✗ {step}")

if results['skipped']:
    print(f"\nSkipped Steps: {len(results['skipped'])}")
    for step in results['skipped']:
        print(f"  ⊘ {step}")

print("\n" + "="*80)
print(" "*30 + "OUTPUT FILES GENERATED")
print("="*80 + "\n")

output_files = {
    'Data Files': [
        'data/cleaned/students.csv',
        'data/cleaned/subjects.csv',
        'data/cleaned/grades.csv',
        'data/cleaned/performance.csv',
        'data/cleaned/subject_performance.csv'
    ],
    'Database': [
        'data/academic_performance.db'
    ],
    'Exports': [
        'data/exports/query_*.csv'
    ],
    'Reports': [
        'docs/reports/cleaning_report.txt',
        'docs/reports/r_statistical_report.txt',
        'ml_models/model_summary.txt'
    ],
    'Visualizations (Python)': [
        'python/outputs/01_sgpa_analysis.png',
        'python/outputs/02_grade_distribution.png',
        'python/outputs/03_subject_performance.png',
        'python/outputs/04_correlation_analysis.png',
        'python/outputs/05_performance_categories.png',
        'python/outputs/06_feature_importance_sgpa.png',
        'python/outputs/07_sgpa_prediction.png',
        'python/outputs/08_confusion_matrix.png'
    ],
    'Visualizations (R)': [
        'r/outputs/01_sgpa_distribution.png',
        'r/outputs/02_sgpa_by_category.png',
        'r/outputs/03_qq_plot.png',
        'r/outputs/04_grade_distribution.png',
        'r/outputs/05_sgpa_vs_grades.png',
        'r/outputs/06_fail_count_vs_sgpa.png'
    ],
    'Machine Learning Models': [
        'ml_models/sgpa_predictor.pkl',
        'ml_models/at_risk_classifier.pkl',
        'ml_models/scaler.pkl'
    ]
}

for category, files in output_files.items():
    print(f"\n{category}:")
    for file_pattern in files:
        if '*' in file_pattern:
            print(f"  • {file_pattern} (multiple files)")
        else:
            exists = "✓" if os.path.exists(file_pattern) else "◌"
            print(f"  {exists} {file_pattern}")

# Final summary
print("\n\n" + "="*80)
print(" "*20 + "ANALYSIS PIPELINE EXECUTION COMPLETE")
print("="*80 + "\n")

if len(results['failed']) == 0:
    print("✓ All steps completed successfully!")
else:
    print(f"⚠️  {len(results['failed'])} step(s) failed. Check error messages above.")

print("\nNext Steps:")
print("  1. Review reports in docs/reports/")
print("  2. View visualizations in python/outputs/ and r/outputs/")
print("  3. Explore SQL results in data/exports/")
print("  4. Check ML models in ml_models/")
print("  5. Query the database at data/academic_performance.db")

print("\n" + "="*80 + "\n")

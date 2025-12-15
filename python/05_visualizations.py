import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
os.makedirs('python/outputs', exist_ok=True)

print("Generating visualizations...\n")

# Load data
performance = pd.read_csv('data/cleaned/performance.csv')
grades = pd.read_csv('data/cleaned/grades.csv')
subjects = pd.read_csv('data/cleaned/subjects.csv')
subject_perf = pd.read_csv('data/cleaned/subject_performance.csv')

# Clean data
performance_clean = performance[performance['sgpa'].notna()]

# VISUALIZATION 1: SGPA Distribution with Statistics
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Histogram
axes[0, 0].hist(performance_clean['sgpa'], bins=15, edgecolor='black', color='steelblue', alpha=0.7)
axes[0, 0].axvline(performance_clean['sgpa'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {performance_clean["sgpa"].mean():.2f}')
axes[0, 0].axvline(performance_clean['sgpa'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {performance_clean["sgpa"].median():.2f}')
axes[0, 0].set_title('SGPA Distribution', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('SGPA')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Boxplot
axes[0, 1].boxplot(performance_clean['sgpa'], vert=True)
axes[0, 1].set_title('SGPA Boxplot', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('SGPA')
axes[0, 1].grid(alpha=0.3)

# Performance category distribution
cat_order = ['Distinction', 'First Class', 'Second Class', 'Pass Class', 'At Risk', 'Promoted']
cat_counts = performance['performance_category'].value_counts().reindex([c for c in cat_order if c in performance['performance_category'].unique()])
axes[1, 0].bar(range(len(cat_counts)), cat_counts.values, color=['gold', 'lightgreen', 'lightblue', 'lightyellow', 'lightcoral', 'lightgray'])
axes[1, 0].set_xticks(range(len(cat_counts)))
axes[1, 0].set_xticklabels(cat_counts.index, rotation=45, ha='right')
axes[1, 0].set_title('Performance Category Distribution', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Count')
axes[1, 0].grid(alpha=0.3)

# Cumulative distribution
sorted_sgpa = np.sort(performance_clean['sgpa'])
cumulative = np.arange(1, len(sorted_sgpa) + 1) / len(sorted_sgpa) * 100
axes[1, 1].plot(sorted_sgpa, cumulative, linewidth=2, color='steelblue')
axes[1, 1].set_title('Cumulative Distribution of SGPA', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('SGPA')
axes[1, 1].set_ylabel('Cumulative Percentage')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('python/outputs/01_sgpa_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: 01_sgpa_analysis.png")
plt.close()

# VISUALIZATION 2: Grade Distribution
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Overall grade distribution
grade_order = ['O', 'A+', 'A', 'B+', 'B', 'C', 'D', 'F']
grade_counts = grades['grade'].value_counts().reindex(grade_order)
colors = ['#2ecc71', '#27ae60', '#3498db', '#2980b9', '#f39c12', '#e67e22', '#e74c3c', '#c0392b']

axes[0].bar(grade_counts.index, grade_counts.values, color=colors, edgecolor='black')
axes[0].set_title('Overall Grade Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Grade')
axes[0].set_ylabel('Count')
for i, v in enumerate(grade_counts.values):
    axes[0].text(i, v + 2, str(v), ha='center', fontweight='bold')

# Grade percentage
grade_pct = (grade_counts / grade_counts.sum() * 100).round(1)
axes[1].pie(grade_pct, labels=grade_pct.index, autopct='%1.1f%%', colors=colors, startangle=90)
axes[1].set_title('Grade Distribution (Percentage)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('python/outputs/02_grade_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: 02_grade_distribution.png")
plt.close()

# VISUALIZATION 3: Subject Performance
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Sort by pass rate
subject_perf_sorted = subject_perf.sort_values('pass_rate')

# Pass rate by subject
colors_pass = ['red' if x < 90 else 'orange' if x < 95 else 'green' for x in subject_perf_sorted['pass_rate']]
axes[0].barh(range(len(subject_perf_sorted)), subject_perf_sorted['pass_rate'], color=colors_pass, edgecolor='black')
axes[0].set_yticks(range(len(subject_perf_sorted)))
axes[0].set_yticklabels(subject_perf_sorted['course_code'], fontsize=9)
axes[0].set_xlabel('Pass Rate (%)')
axes[0].set_title('Pass Rate by Subject', fontsize=14, fontweight='bold')
axes[0].axvline(x=90, color='red', linestyle='--', alpha=0.5, label='90% threshold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Average grade points by subject
subject_perf_sorted2 = subject_perf.sort_values('avg_grade_points')
axes[1].barh(range(len(subject_perf_sorted2)), subject_perf_sorted2['avg_grade_points'], color='steelblue', edgecolor='black')
axes[1].set_yticks(range(len(subject_perf_sorted2)))
axes[1].set_yticklabels(subject_perf_sorted2['course_code'], fontsize=9)
axes[1].set_xlabel('Average Grade Points')
axes[1].set_title('Average Grade Points by Subject (Difficulty)', fontsize=14, fontweight='bold')
axes[1].axvline(x=8, color='green', linestyle='--', alpha=0.5, label='Target (8.0)')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('python/outputs/03_subject_performance.png', dpi=300, bbox_inches='tight')
print("Saved: 03_subject_performance.png")
plt.close()

# Add subject names to y-axis for clarity
fig, axes = plt.subplots(1, 1, figsize=(14, 10))
subject_perf_sorted = subject_perf.sort_values('pass_rate')
subject_display = subject_perf_sorted.apply(lambda x: f"{x['course_code']}\n{x['course_title'][:30]}", axis=1)

colors_pass = ['red' if x < 85 else 'orange' if x < 95 else 'green' for x in subject_perf_sorted['pass_rate']]
axes.barh(range(len(subject_perf_sorted)), subject_perf_sorted['pass_rate'], color=colors_pass, edgecolor='black')
axes.set_yticks(range(len(subject_perf_sorted)))
axes.set_yticklabels(subject_display, fontsize=8)
axes.set_xlabel('Pass Rate (%)', fontsize=12)
axes.set_title('Pass Rate by Subject (Detailed View)', fontsize=14, fontweight='bold')
axes.axvline(x=90, color='red', linestyle='--', alpha=0.5, label='90% threshold')
axes.legend()
axes.grid(alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('python/outputs/03b_subject_performance_detailed.png', dpi=300, bbox_inches='tight')
print("Saved: 03b_subject_performance_detailed.png")
plt.close()

# VISUALIZATION 4: Correlation Analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# SGPA vs Average Grade Points
axes[0].scatter(performance_clean['avg_grade_points'], performance_clean['sgpa'], alpha=0.6, s=100, color='steelblue', edgecolors='black')
z = np.polyfit(performance_clean['avg_grade_points'], performance_clean['sgpa'], 1)
p = np.poly1d(z)
axes[0].plot(performance_clean['avg_grade_points'], p(performance_clean['avg_grade_points']), "r--", linewidth=2)
axes[0].set_xlabel('Average Grade Points')
axes[0].set_ylabel('SGPA')
axes[0].set_title('SGPA vs Average Grade Points', fontsize=14, fontweight='bold')
correlation = performance_clean['avg_grade_points'].corr(performance_clean['sgpa'])
axes[0].text(0.05, 0.95, f'Correlation: {correlation:.3f}', transform=axes[0].transAxes, 
             fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
axes[0].grid(alpha=0.3)

# Fail count vs SGPA
axes[1].scatter(performance_clean['fail_count'], performance_clean['sgpa'], alpha=0.6, s=100, color='coral', edgecolors='black')
axes[1].set_xlabel('Number of Failed Subjects')
axes[1].set_ylabel('SGPA')
axes[1].set_title('SGPA vs Failed Subjects', fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('python/outputs/04_correlation_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: 04_correlation_analysis.png")
plt.close()

# VISUALIZATION 5: Performance Category Breakdown
perf_cat_clean = performance_clean.copy()
fig = plt.figure(figsize=(12, 8))

# Create subplots
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 1, 2)

# Category counts
cat_counts = perf_cat_clean['performance_category'].value_counts()
ax1.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90, 
        colors=['gold', 'lightgreen', 'lightblue', 'lightyellow', 'lightcoral'])
ax1.set_title('Performance Category Distribution')

# SGPA by category (boxplot)
categories = ['Distinction', 'First Class', 'Second Class', 'Pass Class']
data_by_cat = [perf_cat_clean[perf_cat_clean['performance_category'] == cat]['sgpa'].values 
               for cat in categories if cat in perf_cat_clean['performance_category'].unique()]
ax2.boxplot([d for d in data_by_cat if len(d) > 0], labels=[c for c in categories if c in perf_cat_clean['performance_category'].unique()])
ax2.set_title('SGPA Distribution by Category')
ax2.set_ylabel('SGPA')
ax2.tick_params(axis='x', rotation=45)

# Average SGPA by category
cat_means = perf_cat_clean.groupby('performance_category')['sgpa'].mean().sort_values(ascending=False)
ax3.barh(range(len(cat_means)), cat_means.values, color=['gold', 'lightgreen', 'lightblue', 'lightyellow'])
ax3.set_yticks(range(len(cat_means)))
ax3.set_yticklabels(cat_means.index)
ax3.set_xlabel('Average SGPA')
ax3.set_title('Average SGPA by Performance Category')
for i, v in enumerate(cat_means.values):
    ax3.text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')
ax3.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('python/outputs/05_performance_categories.png', dpi=300, bbox_inches='tight')
print("Saved: 05_performance_categories.png")
plt.close()

print("\nAll visualizations saved to python/outputs/")
print("Visualization generation complete!")
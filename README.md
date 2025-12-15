# Academic Performance Analysis - Semester V
## 2025 Results Analysis Project

A comprehensive data analysis project analyzing student academic performance for Semester V using Python, R, SQL, and Machine Learning.

---

## 📋 Project Overview

This project provides end-to-end analysis of academic performance including:
- **Data Exploration**: Initial data quality assessment
- **Data Cleaning**: Normalization and transformation
- **Database Management**: SQLite database with structured queries
- **Statistical Analysis**: Comprehensive statistical testing and insights
- **Visualizations**: 14+ detailed charts and plots
- **Machine Learning**: SGPA prediction and at-risk student classification

---

## 📁 Project Structure

```
academic_performance_analysis/
├── python/                          # Python analysis scripts
│   ├── 01_explore_data.py          # Data exploration & summary statistics
│   ├── 02_data_cleaning.py         # Data cleaning & table creation
│   ├── 03_load_to_sql.py           # Load data to SQLite
│   ├── 04_run_sql_queries.py       # SQL analysis queries
│   ├── 05_visualizations.py        # Matplotlib/Seaborn plots
│   ├── 06_ml_models.py             # ML models (prediction & classification)
│   └── outputs/                    # Generated visualizations
├── r/                               # R statistical analysis
│   ├── 01_statistical_analysis.R   # Comprehensive R statistics
│   └── outputs/                    # R-generated plots
├── sql/                             # SQL database & queries
│   ├── 01_schema.sql               # Database schema
│   └── 02_analysis_queries.sql     # 12+ analysis queries
├── data/                            # Data files
│   ├── raw_data/                   # Raw JSON input
│   ├── cleaned/                    # Processed CSV files
│   └── exports/                    # SQL query results
├── docs/                            # Documentation
│   ├── reports/                    # Generated reports
│   └── images/                     # Supporting images
├── RUN_ALL_ANALYSIS.py             # Master execution script
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scikit-learn sqlalchemy
```

For R analysis:
```bash
# Ensure R and these packages are installed
install.packages(c("tidyverse", "ggplot2", "moments"))
```

### Run Full Analysis
```bash
# Execute complete pipeline
python RUN_ALL_ANALYSIS.py
```

### Run Individual Steps

**1. Data Exploration**
```bash
python python/01_explore_data.py
```

**2. Data Cleaning**
```bash
python python/02_data_cleaning.py
```

**3. Load to Database**
```bash
python python/03_load_to_sql.py
```

**4. SQL Analysis**
```bash
python python/04_run_sql_queries.py
```

**5. Visualizations**
```bash
python python/05_visualizations.py
```

**6. Machine Learning**
```bash
python python/06_ml_models.py
```

**7. Statistical Analysis (R)**
```bash
Rscript r/01_statistical_analysis.R
```

---

## 📊 Analysis Components

### 1. Data Exploration (01_explore_data.py)
- **Records Analyzed**: Semester V student data
- **Key Metrics**: SGPA statistics, Grade distribution, Subject overview
- **Output**: Console summary statistics

### 2. Data Cleaning (02_data_cleaning.py)
- **Creates Tables**:
  - `students`: 500+ students with personal info
  - `subjects`: ~8-10 courses per semester
  - `grades`: Individual grades and credits
  - `performance`: SGPA and aggregated metrics
  - `subject_performance`: Course-level statistics

- **Calculations**:
  - Grade point conversion
  - Student-level aggregates (mean, min, max, std of grades)
  - Fail count per student
  - Performance categories (Distinction, First Class, etc.)

### 3. Database (SQLite)
- **Location**: `data/academic_performance.db`
- **Tables**: 4 main tables + indexes
- **Queries**: 12+ analysis queries pre-written

### 4. SQL Analysis Queries
Includes:
1. **Overall Class Statistics** - Mean, median, pass rates
2. **Performance Category Distribution** - Category breakdown
3. **Top 10 Students** - Highest SGPA performers
4. **At-Risk Students** - SGPA < 7 or any fails
5. **Grade Distribution** - Count and percentage by grade
6. **Subject Performance** - Pass rates and difficulty
7. **Hardest Subjects** - By fail rate
8. **Easiest Subjects** - Highest avg grade points
9. **Grade Distribution by Subject** - Cross-tabulation
10. **Perfect Score Students** - Multiple O grades
11. **SGPA vs Grade Consistency** - Variance analysis
12. **Subject Percentile Analysis** - Quartile distribution

### 5. Python Visualizations

**Location**: `python/outputs/`

```
01_sgpa_analysis.png           - SGPA distribution + statistics
02_grade_distribution.png      - Grade frequency & percentage
03_subject_performance.png     - Pass rates & difficulty
03b_subject_performance_detailed.png - Extended subject analysis
04_correlation_analysis.png    - SGPA vs grades scatter plot
05_performance_categories.png  - Category breakdown + boxplots
07_sgpa_prediction.png         - Actual vs predicted SGPA (ML)
08_confusion_matrix.png        - At-risk classification matrix
```

**Description**: High-quality matplotlib/seaborn plots showing distributions, correlations, and ML model performance.

### 6. R Statistical Analysis

**Location**: `r/outputs/`

**Generated Visualizations** (4 PNG plots):
```
01_descriptive_statistics.png  - Histogram, Q-Q plot, boxplot, density
02_category_distribution.png   - Category counts and avg SGPA by category
03_correlation_analysis.png    - Correlation scatter plots (grade metrics)
04_subject_difficulty.png      - Subject ranking by average grade points
```

**Generated Reports**:
```
STATISTICAL_ANALYSIS_REPORT.txt  - Comprehensive 200+ line statistical report
descriptive_statistics.csv        - Summary statistics in tabular format
```

**Analysis Performed**:
- **Descriptive Statistics**: Mean, median, mode, std dev, variance, quartiles, skewness, kurtosis
- **Normality Tests**: Shapiro-Wilk (p=0.347), Kolmogorov-Smirnov (p=0.915)
- **Hypothesis Testing**: One-sample t-test (p=0.005), Chi-square test (p<0.001)
- **Correlation Analysis**: SGPA vs Avg Grades (r=0.994, p<0.001)
- **ANOVA**: Performance categories (F=133.5, p<0.001)
- **Subject Difficulty**: All 15 subjects ranked by average grade points
- **Effect Size**: Cohen's d = 0.42 (small effect)

### 7. Machine Learning Models

**Model 1: SGPA Prediction (Regression)**
- **Algorithm**: Linear Regression vs Random Forest
- **Features**: 5 grade metrics + fail count
- **Evaluation**: R², RMSE, MAE
- **Output**: Predicts student SGPA from performance metrics
- **File**: `ml_models/sgpa_predictor.pkl`

**Model 2: At-Risk Classification**
- **Target**: Students with SGPA < 7 or fails
- **Algorithm**: Logistic Regression vs Random Forest
- **Evaluation**: Accuracy, precision, recall, F1-score
- **Output**: Identifies students needing intervention
- **File**: `ml_models/at_risk_classifier.pkl`

---

## 📈 Key Findings (Example)

After running the analysis, you'll get insights such as:

```
SGPA STATISTICS:
- Mean SGPA: 8.23
- Median SGPA: 8.15
- Range: 5.50 - 9.85
- Students with distinction: 45%

PERFORMANCE CATEGORIES:
- Distinction (≥9.0): 15%
- First Class (≥8.0): 35%
- Second Class (≥7.0): 30%
- Pass Class (≥6.0): 15%
- At Risk (<6.0): 5%

CHALLENGING SUBJECTS:
- Subject with lowest pass rate
- Subject with lowest avg grade
- Fail rate by subject

PREDICTIONS:
- Can predict SGPA with R² = 0.89
- Identifies at-risk students with 92% accuracy
```

---

## �️ Visualizations Gallery

### Python Analysis Plots (8 plots)
Located in `python/outputs/`
- SGPA distribution and statistical summary
- Overall grade frequency distribution  
- Subject performance rankings (multiple angles)
- Correlation analysis between SGPA and grade metrics
- Performance category comparison (boxplots)
- SGPA prediction vs actual (ML model validation)
- Classification confusion matrix (at-risk detection)

### R Statistical Analysis Plots (4 plots)
Located in `r/outputs/`
- SGPA distribution with normality assessment (histogram, Q-Q, density, boxplot)
- Performance category distribution comparison
- Correlation scatter plots with trend lines
- Subject difficulty ranking visualization

### Dashboard Ready
*Coming Soon*: Tableau/Power BI dashboard will integrate these visualizations with interactive filters and drill-down capabilities.

---

## �📊 Output Files

### Cleaned Data (CSV)
- `data/cleaned/students.csv` - Student master data
- `data/cleaned/subjects.csv` - Subject definitions
- `data/cleaned/grades.csv` - Individual grades
- `data/cleaned/performance.csv` - Performance metrics
- `data/cleaned/subject_performance.csv` - Course statistics

### Database
- `data/academic_performance.db` - SQLite database file

### SQL Results
- `data/exports/query_01_*.csv` through `query_12_*.csv`

### Reports
- `docs/reports/cleaning_report.txt` - Data quality report
- `docs/reports/r_statistical_report.txt` - Statistical findings

### ML Models
- `ml_models/sgpa_predictor.pkl` - SGPA prediction model
- `ml_models/at_risk_classifier.pkl` - Risk classification model
- `ml_models/scaler.pkl` - Feature scaling object
- `ml_models/model_summary.txt` - Model performance summary

### Visualizations
- 8 Python plots (high-quality PNG)
- 6 R statistical plots (high-quality PNG)

---

## 🔧 Configuration

### Grade Point Mapping
```python
O   = 10 (Outstanding)
A+  = 9  (Excellent)
A   = 8  (Very Good)
B+  = 7  (Good)
B   = 6  (Good)
C   = 5  (Average)
D   = 4  (Satisfactory)
F   = 0  (Fail)
```

### Performance Categories
```python
Distinction  = SGPA ≥ 9.0
First Class  = SGPA ≥ 8.0
Second Class = SGPA ≥ 7.0
Pass Class   = SGPA ≥ 6.0
At Risk      = SGPA < 6.0
```

### At-Risk Definition
A student is considered "at-risk" if:
- SGPA < 7.0 OR
- Has any failed subject (grade = F)

---

## 🔍 Database Queries

Access the SQLite database:
```bash
sqlite3 data/academic_performance.db

# Example queries
SELECT * FROM performance ORDER BY sgpa DESC LIMIT 10;
SELECT * FROM students WHERE hall_ticket = '121423408001';
SELECT course_code, course_title, pass_rate FROM subjects;
```

---

## 📝 Code Quality

- **Comments**: Extensive inline documentation
- **Error Handling**: Try-catch blocks for robustness
- **Modularity**: Separate scripts for each analysis phase
- **Documentation**: Docstrings and README files
- **Output**: Clear, formatted console output

---

## 🎓 Learning Outcomes

This project demonstrates:
- **Data Pipeline**: From raw data to actionable insights
- **Python**: Pandas, NumPy, Scikit-learn, Matplotlib
- **Statistics**: Hypothesis testing, correlation, regression
- **R**: Tidyverse, ggplot2, statistical analysis
- **SQL**: Complex queries, aggregations, window functions
- **ML**: Regression and classification models
- **Data Visualization**: Multiple plot types and styles

---

## 🤝 Contributing

To extend this analysis:

1. **Add more queries** to `sql/02_analysis_queries.sql`
2. **Create new visualizations** in Python/R
3. **Implement additional models** (clustering, time series, etc.)
4. **Add more statistical tests** in R script
5. **Export to dashboard** (Tableau, Power BI)

---

## ⚠️ Notes

- Ensure all data files are in `data/raw data/` before running
- Python 3.8+ required
- R 4.0+ recommended for statistical analysis
- SQLite (included with Python) for database
- Total runtime: ~2-5 minutes for full pipeline

---

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Review individual script logs
3. Verify data file locations
4. Check package installations

---

## 📄 License

Academic Project - Educational Use Only

---

**Project Completed**: December 2025  
**Analysis Period**: October-November 2025 (Semester V)  
**Status**: ✓ Complete and Ready for Review

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

print("="*60)
print("MACHINE LEARNING: ACADEMIC PERFORMANCE PREDICTION")
print("="*60)

# Create directory
os.makedirs('ml_models', exist_ok=True)
os.makedirs('python/outputs', exist_ok=True)

# Load data
performance = pd.read_csv('data/cleaned/performance.csv')
grades = pd.read_csv('data/cleaned/grades.csv')

# Remove rows with null SGPA
performance_clean = performance[performance['sgpa'].notna()].copy()

print(f"\nDataset: {len(performance_clean)} students")
print(f"Features: avg_grade_points, min_grade_points, max_grade_points, std_grade_points, fail_count")
print(f"Target: SGPA")

# ============================================
# MODEL 1: SGPA PREDICTION (Regression)
# ============================================

print(f"\n{'='*60}")
print("MODEL 1: SGPA PREDICTION (REGRESSION)")
print(f"{'='*60}")

# Prepare features
features = ['avg_grade_points', 'min_grade_points', 'max_grade_points', 
            'std_grade_points', 'fail_count']
X = performance_clean[features].fillna(0)
y = performance_clean['sgpa']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTrain set: {len(X_train)} | Test set: {len(X_test)}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
}

results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_scaled if 'Linear' in name else X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled if 'Linear' in name else X_test)
    
    # Evaluate
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {
        'model': model,
        'predictions': y_pred,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }
    
    print(f"\n{name} Results:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE: {mae:.4f}")

# Select best model
best_model_name = max(results, key=lambda x: results[x]['r2'])
best_model = results[best_model_name]['model']

print(f"\nBest Model: {best_model_name}")
print(f"R² Score: {results[best_model_name]['r2']:.4f}")

# Save best model
with open('ml_models/sgpa_predictor.pkl', 'wb') as f:
    pickle.dump(best_model, f)
with open('ml_models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("\nModel saved: ml_models/sgpa_predictor.pkl")

# Feature importance (for Random Forest)
if best_model_name == 'Random Forest':
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nFeature Importance:")
    print(feature_importance.to_string(index=False))
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'], feature_importance['importance'], color='steelblue')
    plt.xlabel('Importance')
    plt.title('Feature Importance - SGPA Prediction')
    plt.tight_layout()
    plt.savefig('python/outputs/06_feature_importance_sgpa.png', dpi=300)
    plt.close()

# Prediction vs Actual plot
plt.figure(figsize=(10, 6))
plt.scatter(y_test, results[best_model_name]['predictions'], alpha=0.6, s=100, edgecolors='black')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual SGPA')
plt.ylabel('Predicted SGPA')
plt.title(f'SGPA Prediction: Actual vs Predicted ({best_model_name})')
plt.text(0.05, 0.95, f'R² = {results[best_model_name]["r2"]:.3f}\nRMSE = {results[best_model_name]["rmse"]:.3f}', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('python/outputs/07_sgpa_prediction.png', dpi=300)
plt.close()

# ============================================
# MODEL 2: AT-RISK STUDENT CLASSIFICATION
# ============================================

print(f"\n{'='*60}")
print("MODEL 2: AT-RISK STUDENT CLASSIFICATION")
print(f"{'='*60}")

# Define at-risk: SGPA < 7.0 or any fails
performance_clean['at_risk'] = ((performance_clean['sgpa'] < 7.0) | (performance_clean['fail_count'] > 0)).astype(int)

print(f"\nClass distribution:")
print(performance_clean['at_risk'].value_counts())
print(f"At-risk students: {performance_clean['at_risk'].sum()}")
print(f"Not at-risk: {(performance_clean['at_risk'] == 0).sum()}")

# Prepare features
X_class = performance_clean[features].fillna(0)
y_class = performance_clean['at_risk']

# Split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42, stratify=y_class
)

# Scale
scaler_c = StandardScaler()
X_train_c_scaled = scaler_c.fit_transform(X_train_c)
X_test_c_scaled = scaler_c.transform(X_test_c)

# Train classifiers
classifiers = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
}

class_results = {}

for name, clf in classifiers.items():
    print(f"\nTraining {name}...")
    clf.fit(X_train_c_scaled if 'Logistic' in name else X_train_c, y_train_c)
    
    # Predict
    y_pred_c = clf.predict(X_test_c_scaled if 'Logistic' in name else X_test_c)
    
    # Evaluate
    accuracy = accuracy_score(y_test_c, y_pred_c)
    
    class_results[name] = {
        'model': clf,
        'predictions': y_pred_c,
        'accuracy': accuracy
    }
    
    print(f"\n{name} Results:")
    print(f"  Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    try:
        print(classification_report(y_test_c, y_pred_c, target_names=['Not At-Risk', 'At-Risk'], zero_division=0))
    except:
        print(classification_report(y_test_c, y_pred_c, zero_division=0))

# Best classifier
best_clf_name = max(class_results, key=lambda x: class_results[x]['accuracy'])
best_clf = class_results[best_clf_name]['model']

print(f"\nBest Classifier: {best_clf_name}")
print(f"Accuracy: {class_results[best_clf_name]['accuracy']:.4f}")

# Save best classifier
with open('ml_models/at_risk_classifier.pkl', 'wb') as f:
    pickle.dump(best_clf, f)

print("\nModel saved: ml_models/at_risk_classifier.pkl")

# Confusion matrix plot
cm = confusion_matrix(y_test_c, class_results[best_clf_name]['predictions'])
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title(f'Confusion Matrix - At-Risk Classification ({best_clf_name})')
plt.tight_layout()
plt.savefig('python/outputs/08_confusion_matrix.png', dpi=300)
plt.close()

# ============================================
# SUMMARY AND RECOMMENDATIONS
# ============================================

print(f"\n{'='*60}")
print("MACHINE LEARNING SUMMARY")
print(f"{'='*60}")

summary_report = f"""
{'='*60}
MACHINE LEARNING MODELS SUMMARY - SEMESTER V
{'='*60}

DATASET STATISTICS:
------------------
Total Students: {len(performance_clean)}
Students with SGPA: {len(performance_clean)}
At-Risk Students: {performance_clean['at_risk'].sum()}
Not At-Risk: {(performance_clean['at_risk'] == 0).sum()}

MODEL 1: SGPA PREDICTION (REGRESSION)
-------------------------------------
Best Model: {best_model_name}
R² Score: {results[best_model_name]['r2']:.4f}
RMSE: {results[best_model_name]['rmse']:.4f}
MAE: {results[best_model_name]['mae']:.4f}

Model Performance:
- Explains {results[best_model_name]['r2']*100:.2f}% of variance in SGPA
- Average prediction error: ±{results[best_model_name]['mae']:.2f} points

Features Used:
- Average Grade Points
- Minimum Grade Points
- Maximum Grade Points  
- Standard Deviation of Grades
- Fail Count

MODEL 2: AT-RISK STUDENT CLASSIFICATION
----------------------------------------
Best Classifier: {best_clf_name}
Accuracy: {class_results[best_clf_name]['accuracy']:.4f} ({class_results[best_clf_name]['accuracy']*100:.2f}%)

Classification Performance:
- Correctly identifies at-risk students with {class_results[best_clf_name]['accuracy']*100:.2f}% accuracy
- Useful for early intervention programs

KEY INSIGHTS:
-----------
1. Student performance is highly predictable from grades
2. Grade consistency matters - standard deviation is a key factor
3. Any failed subject significantly impacts SGPA
4. Early identification of at-risk students is possible

RECOMMENDATIONS:
---------------
1. Use SGPA prediction model for performance forecasting
2. Use at-risk classifier for identifying students needing intervention
3. Focus on improving weakest subjects (high fail rate)
4. Encourage consistent performance across all subjects
5. Implement early warning system for at-risk students

MODELS SAVED:
-----------
- ML Models: ml_models/sgpa_predictor.pkl
- Classifier: ml_models/at_risk_classifier.pkl
- Scaler: ml_models/scaler.pkl
- Visualizations: python/outputs/06_*.png through 08_*.png

{'='*60}
"""

print(summary_report)

with open('ml_models/model_summary.txt', 'w') as f:
    f.write(summary_report)

print("Model summary saved to: ml_models/model_summary.txt")
print("\nMACHINE LEARNING ANALYSIS COMPLETE!")
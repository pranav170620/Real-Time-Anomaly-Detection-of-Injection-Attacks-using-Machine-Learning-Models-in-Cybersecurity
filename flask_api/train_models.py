from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the datasets
df_sql = pd.read_csv('C:/Users/S Pranav Kumar/Anomaly-Detection-SQL-Injection/AnomalyDetection/SQL_Queries_Dataset.csv')
df_xss = pd.read_csv('C:/Users/S Pranav Kumar/Anomaly-Detection-SQL-Injection/AnomalyDetection/XSS_Injection_Dataset.csv')

# Preprocess SQL Injection Data
X_sql = df_sql['Query Text']
y_sql = df_sql['Risk Level']

X_train_sql, X_test_sql, y_train_sql, y_test_sql = train_test_split(X_sql, y_sql, test_size=0.3, random_state=42)

vectorizer_sql = TfidfVectorizer()
X_train_sql_vec = vectorizer_sql.fit_transform(X_train_sql)
X_test_sql_vec = vectorizer_sql.transform(X_test_sql)

# Preprocess XSS Injection Data
X_xss = df_xss['Input Text']
y_xss = df_xss['Risk Level']

X_train_xss, X_test_xss, y_train_xss, y_test_xss = train_test_split(X_xss, y_xss, test_size=0.3, random_state=42)

vectorizer_xss = TfidfVectorizer()
X_train_xss_vec = vectorizer_xss.fit_transform(X_train_xss)
X_test_xss_vec = vectorizer_xss.transform(X_test_xss)

# Train SQL Injection Models
rf_classifier_sql = RandomForestClassifier(random_state=42)
dt_classifier_sql = DecisionTreeClassifier(random_state=42)

# Ensemble Model
ensemble_sql = VotingClassifier(estimators=[
    ('rf', rf_classifier_sql),
    ('dt', dt_classifier_sql)
], voting='soft')

ensemble_sql.fit(X_train_sql_vec, y_train_sql)

# Train XSS Injection Models
rf_classifier_xss = RandomForestClassifier(random_state=42)
dt_classifier_xss = DecisionTreeClassifier(random_state=42)

# Ensemble Model
ensemble_xss = VotingClassifier(estimators=[
    ('rf', rf_classifier_xss),
    ('dt', dt_classifier_xss)
], voting='soft')

ensemble_xss.fit(X_train_xss_vec, y_train_xss)

# Save models
joblib.dump(ensemble_sql, 'ensemble_model_sql.pkl')
joblib.dump(ensemble_xss, 'ensemble_model_xss.pkl')
joblib.dump(vectorizer_sql, 'vectorizer_sql.pkl')
joblib.dump(vectorizer_xss, 'vectorizer_xss.pkl')

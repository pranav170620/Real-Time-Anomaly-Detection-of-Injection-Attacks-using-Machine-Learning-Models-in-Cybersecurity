from flask_socketio import SocketIO, emit
from flask import Flask, request, jsonify, render_template
import joblib
import logging
import psutil
import pandas as pd
from sklearn.metrics import accuracy_score
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Load the actual datasets
df_sql = pd.read_csv('C:/Users/S Pranav Kumar/Anomaly-Detection-SQL-Injection/AnomalyDetection/SQL_Queries_Dataset.csv')
df_xss = pd.read_csv('C:/Users/S Pranav Kumar/Anomaly-Detection-SQL-Injection/AnomalyDetection/XSS_Injection_Dataset.csv')

# Ensure that the 'Timestamp' column is correctly formatted as datetime
df_sql['Timestamp'] = pd.to_datetime(df_sql['Timestamp'])
df_xss['Timestamp'] = pd.to_datetime(df_xss['Timestamp'])

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the models and vectorizers
try:
    # Load ensemble models
    ensemble_model_sql = joblib.load('ensemble_model_sql.pkl')
    ensemble_model_xss = joblib.load('ensemble_model_xss.pkl')
    vectorizer_sql = joblib.load('vectorizer_sql.pkl')
    vectorizer_xss = joblib.load('vectorizer_xss.pkl')

except Exception as e:
    logging.error(f"Error loading models or vectorizer: {e}")
    raise e

# Initialize counters for real-time updates
sql_injection_count = 0
xss_injection_count = 0
recent_alerts_list = []

# Load saved state from alerts.json if available
alerts_file = "alerts.json"
if os.path.exists(alerts_file):
    try:
        with open(alerts_file, "r") as f:
            state = json.load(f)
            if isinstance(state, dict):
                sql_injection_count = state.get("sql_injection_count", 0)
                xss_injection_count = state.get("xss_injection_count", 0)
                recent_alerts_list = state.get("recent_alerts_list", [])
            else:
                print("Warning: alerts.json is not a valid dictionary. Resetting state.")
                state = {}
    except json.JSONDecodeError:
        print("Error: alerts.json is not a valid JSON. Resetting state.")
        state = {}
else:
    state = {}

# Refined function to detect the attack type
def detect_attack_type(query):
    query_lower = query.lower().strip()

    # XSS Detection
    if query_lower.startswith("<") or query_lower.startswith("javascript") or any(tag in query_lower for tag in ["<script>", "<img", "<iframe", "onerror", "onload"]):
        return "XSS"

    # SQL Injection Detection
    sql_keywords = ["'", " or ", "--", "union", "select", "drop", "insert", "update", "delete", "where"]
    if any(sql_keyword in query_lower for sql_keyword in sql_keywords):
        return "SQL"

    # Default to SQL if unsure
    return "SQL"

def calculate_detection_accuracy():
    # SQL Injection Accuracy
    X_sql = vectorizer_sql.transform(df_sql['Query Text'])
    y_sql_true = df_sql['Risk Level']
    y_sql_pred = ensemble_model_sql.predict(X_sql)

    # XSS Injection Accuracy
    X_xss = vectorizer_xss.transform(df_xss['Input Text'])
    y_xss_true = df_xss['Risk Level']
    y_xss_pred = ensemble_model_xss.predict(X_xss)

    # Calculate accuracy
    sql_accuracy = accuracy_score(y_sql_true, y_sql_pred)
    xss_accuracy = accuracy_score(y_xss_true, y_xss_pred)

    # Average accuracy across all models
    overall_accuracy = (sql_accuracy + xss_accuracy) / 2

    return overall_accuracy * 100

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    global sql_injection_count, xss_injection_count

    try:
        data = request.json
        query_text = data.get('queryText')

        if not query_text:
            return jsonify({"error": "No query text provided"}), 400

        attack_type = detect_attack_type(query_text)

        if attack_type == "SQL":
            query_vectorized = vectorizer_sql.transform([query_text])
            risk_level = ensemble_model_sql.predict(query_vectorized)[0]
            insight = "The query contains patterns similar to SQL injection."
            sql_injection_count += 1  # Update the SQL injection count
        else:
            query_vectorized = vectorizer_xss.transform([query_text])
            risk_level = ensemble_model_xss.predict(query_vectorized)[0]
            insight = "The query contains patterns similar to XSS injection."
            xss_injection_count += 1  # Update the XSS injection count

        result = {
            "Risk Level": risk_level,
            "Consequence": "Potential data breach",
            "Insight": insight,
            "Attack Type": attack_type
        }

        # Log the alert for recent alerts
        recent_alert = {
            "timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            "type": attack_type,
            "severity": risk_level,
            "action": "Blocked" if risk_level in ['High', 'Medium'] else "Logged"
        }
        recent_alerts_list.append(recent_alert)  # Store the alert in recent_alerts_list

        # Emit the update to the clients with the new data for the chart
        socketio.emit('update_chart', {
            "sql_count": sql_injection_count,
            "xss_count": xss_injection_count,
            "timestamp": pd.Timestamp.now().strftime('%H:%M')  # This is the correct format
        })

        # Emit updated historical data
        emit_updated_historical_data()

        # Check for critical alerts and emit them
        if risk_level == 'High':
            alert_message = f'Critical {attack_type} attack detected!!!!'
            socketio.emit('alert', {'message': alert_message, 'severity': 'critical'})


        # Save state to alerts.json
        with open(alerts_file, "w") as f:
            json.dump({
                "sql_injection_count": sql_injection_count,
                "xss_injection_count": xss_injection_count,
                "recent_alerts_list": recent_alerts_list
            }, f)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

def emit_updated_historical_data():
    # Prepare SQL historical data
    sql_historical_data = df_sql.groupby(pd.to_datetime(df_sql['Timestamp']).dt.date).size().to_list()

    # Prepare XSS historical data
    xss_historical_data = df_xss.groupby(pd.to_datetime(df_xss['Timestamp']).dt.date).size().to_list()

    # Emit both datasets to the frontend
    socketio.emit('update_historical_data', {
        "sql_historical_data": sql_historical_data,
        "xss_historical_data": xss_historical_data,
    })

@app.route('/sql_injection_stats')
def sql_injection_stats():
    total_attempts = len(df_sql)
    critical_alerts = len(df_sql[df_sql['Risk Level'] == 'High'])
    resolved_issues = total_attempts - critical_alerts

    trend_data = df_sql['Risk Level'].value_counts().tolist()

    stats = {
        "total_attempts": total_attempts,
        "critical_alerts": critical_alerts,
        "resolved_issues": resolved_issues,
        "trend_data": trend_data
    }
    return jsonify(stats)

@app.route('/xss_injection_stats')
def xss_injection_stats():
    total_attempts = len(df_xss)
    critical_alerts = len(df_xss[df_xss['Risk Level'] == 'High'])
    resolved_issues = total_attempts - critical_alerts

    trend_data = df_xss['Risk Level'].value_counts().tolist()

    stats = {
        "total_attempts": total_attempts,
        "critical_alerts": critical_alerts,
        "resolved_issues": resolved_issues,
        "trend_data": trend_data
    }
    return jsonify(stats)

@app.route('/sql_anomaly_reports_data')
def sql_anomaly_reports_data():
    sql_anomaly_data = df_sql['Risk Level'].value_counts().to_dict()

    data = {
        "labels": list(sql_anomaly_data.keys()),
        "values": list(sql_anomaly_data.values())
    }
    return jsonify(data)

@app.route('/sql_historical_data')
def sql_historical_data():
    sql_data = df_sql.groupby(pd.to_datetime(df_sql['Timestamp']).dt.date).size()

    data = {
        "labels": sql_data.index.astype(str).tolist(),
        "values": sql_data.values.tolist()
    }

    return jsonify(data)

@app.route('/xss_historical_data')
def xss_historical_data():
    xss_data = df_xss.groupby(pd.to_datetime(df_xss['Timestamp']).dt.date).size()

    data = {
        "labels": xss_data.index.astype(str).tolist(),
        "values": xss_data.values.tolist()
    }

    return jsonify(data)


@app.route('/xss_anomaly_reports_data')
def xss_anomaly_reports_data():
    xss_anomaly_data = df_xss['Risk Level'].value_counts().to_dict()

    data = {
        "labels": list(xss_anomaly_data.keys()),
        "values": list(xss_anomaly_data.values())
    }
    return jsonify(data)

@app.route('/risk_distribution_data')
def risk_distribution_data():
    return jsonify({"sql_count": sql_injection_count, "xss_count": xss_injection_count})

@app.route('/system_performance')
def system_performance():
    detection_accuracy = calculate_detection_accuracy()

    performance = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "detection_accuracy": detection_accuracy
    }
    return jsonify(performance)

@app.route('/recent_alerts')
def recent_alerts():
    return jsonify(recent_alerts_list[-10:])  # Return the last 10 alerts

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


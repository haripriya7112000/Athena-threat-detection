from flask import Flask, request, jsonify
import joblib
import numpy as np
import traceback
import os
import csv
from datetime import datetime
from colorama import Fore, Style
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load model and scaler
model = joblib.load('../models/best_random_forest_model.pkl')
scaler = joblib.load('../models/scaler.pkl')

# Log prediction classes for verification
print("✅ Model classes:", model.classes_)

# Ensure logs directory exists
os.makedirs('../logs', exist_ok=True)

# Setup log file path
log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/prediction_log.csv'))

# Create header if log file doesn't exist
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as f:
        header = ['timestamp'] + [f"feature_{i+1}" for i in range(78)] + ['prediction']
        writer = csv.writer(f)
        writer.writerow(header)

# Setup alerts directory and log
alert_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../alerts/alerts_log.txt'))
os.makedirs(os.path.dirname(alert_log), exist_ok=True)

def log_alert(message):
    print(Fore.RED + "🚨 ALERT: " + message + Style.RESET_ALL)
    with open(alert_log, 'a') as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

@app.route('/')
def home():
    return "Athena Threat Detection API is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        features = input_data.get('features')

        if features is None:
            return jsonify({'error': 'Missing "features" key in input data'}), 400

        print("📦 Input received with length:", len(features))
        if len(features) != 78:
            return jsonify({'error': f'Expected 78 features, got {len(features)}'}), 400

        # Convert and scale
        features_np = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_np)

        print("✅ Scaled input preview:", features_scaled[0][:5])

        # Predict
        prediction = int(model.predict(features_scaled)[0])
        print("🎯 Prediction result:", prediction)

        # Simulate alert
        if prediction == -1:
            log_alert("DDoS Attack detected from incoming feature vector.")

        # Log to CSV
        with open(log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().isoformat()
            row = [timestamp] + list(map(str, features[:78])) + [str(prediction)]
            writer.writerow(row)

        return jsonify({'prediction': prediction})

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)


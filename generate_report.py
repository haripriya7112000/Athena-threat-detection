# generate_report.py - Tabular Summary of Prediction Results

import pandas as pd
import os
from datetime import datetime
from tabulate import tabulate

# Load prediction log
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/prediction_log.csv'))
report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../reports/prediction_summary_report.txt'))
os.makedirs(os.path.dirname(report_path), exist_ok=True)

if not os.path.exists(log_path):
    print("❌ No prediction_log.csv found. Please run predictions first.")
    exit()

# Read log
df = pd.read_csv(log_path)

# Convert timestamp
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# Summary counts
total_preds = len(df)
benign_count = (df['prediction'] == 0).sum()
ddos_count = (df['prediction'] == -1).sum()

# Most recent predictions (last 5)
recent = df.tail(5)[['timestamp', 'prediction']]

# Write report in tabular format
with open(report_path, 'w') as f:
    f.write("Athena Threat Detection - Prediction Summary Report\n")
    f.write("="*60 + "\n")
    f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"Total Predictions Made: {total_preds}\n")
    f.write(f"Benign (0): {benign_count}\n")
    f.write(f"DDoS   (-1): {ddos_count}\n\n")
    f.write("Most Recent Predictions (Tabular View):\n")
    f.write(tabulate(recent, headers='keys', tablefmt='grid'))

print(f"✅ Report saved to: {report_path}")

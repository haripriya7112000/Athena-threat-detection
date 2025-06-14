import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import ast

st.set_page_config(page_title="Athena Threat Detection Dashboard", layout="wide")

st.title("🛡️ Athena Threat Detection Dashboard")

# Upload CSV for prediction
uploaded_file = st.file_uploader("📤 Upload a test CSV file (78 features)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully")

    predictions = []
    for i, row in enumerate(df.values):
        if len(row) != 78:
            st.error(f"❌ Row {i+1} skipped: Expected 78 features, got {len(row)}")
            predictions.append(None)
            continue

        try:
            response = requests.post(
                url="http://127.0.0.1:5000/predict",
                json={"features": list(row)}
            )
            result = response.json()
            predictions.append(result.get("prediction"))
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API request failed: {e}")
            predictions.append(None)

    df['Prediction'] = predictions
    st.write("### 🔍 Prediction Results")
    st.dataframe(df)

    # Save predictions with timestamp to prediction_log.csv
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/prediction_log.csv'))
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    feature_count = 78
    header = ["timestamp"] + [f"feature_{i+1}" for i in range(feature_count)] + ["prediction"]

    # Write new header
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            f.write(",".join(header) + "\n")

    # Append predictions safely
    with open(log_path, 'a') as f:
        for row, pred in zip(df.iloc[:, :-1].values, predictions):
            if pred is None:
                continue  # Skip rows with invalid prediction
            row = list(map(str, row))[:feature_count]  # Ensure fixed length
            values = [datetime.now().isoformat()] + row + [str(pred)]
            f.write(",".join(values) + "\n")

    # Add toggle to show charts and summary
    if st.button("📊 Display Chart and Summary Report"):
        st.markdown("---")
        st.header("📈 Prediction Summary and Visualizations")

        if os.path.exists(log_path):
            try:
                # Fix rows with lists as strings
                fixed_lines = []
                with open(log_path, 'r') as f:
                    for line in f:
                        if line.count(',') < feature_count + 2 and '[' in line:
                            parts = line.strip().split(',"')
                            timestamp = parts[0]
                            feature_list_str = parts[1].split('"')[0]
                            features = ast.literal_eval(feature_list_str)
                            prediction = parts[1].split('"')[-1].replace(',', '').strip()
                            fixed_lines.append(
                                [timestamp] + list(map(str, features))[:feature_count] + [prediction]
                            )
                        else:
                            fixed_lines.append(line.strip().split(','))

                log_df = pd.DataFrame(fixed_lines[1:], columns=fixed_lines[0])
                log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
                log_df['prediction'] = log_df['prediction'].astype(int)

                # Date range filter
                date_range = st.sidebar.date_input("📅 Filter by Date", [])
                if len(date_range) == 2:
                    log_df = log_df[(log_df['timestamp'].dt.date >= date_range[0]) & (log_df['timestamp'].dt.date <= date_range[1])]

                # Count summary
                st.markdown("### 🔢 Prediction Counts")
                pred_counts = log_df['prediction'].value_counts().rename(index={0: 'Benign (0)', -1: 'DDoS (-1)'})
                st.dataframe(pred_counts.reset_index().rename(columns={'index': 'Prediction', 'prediction': 'Count'}))

                # Bar chart
                fig1, ax1 = plt.subplots()
                sns.countplot(data=log_df, x='prediction', palette='Set2', ax=ax1)
                ax1.set_title("Prediction Distribution")
                ax1.set_xlabel("Prediction")
                ax1.set_ylabel("Count")
                st.pyplot(fig1)

                # Time series chart
                st.markdown("### 🕒 Predictions Over Time")
                log_df['minute'] = log_df['timestamp'].dt.floor('min')
                ts = log_df.groupby(['minute', 'prediction']).size().unstack(fill_value=0)
                fig2, ax2 = plt.subplots(figsize=(10, 4))
                ts.plot(ax=ax2, marker='o')
                ax2.set_ylabel("Count")
                ax2.set_xlabel("Time (per minute)")
                ax2.set_title("Predictions Over Time")
                st.pyplot(fig2)
            except Exception as e:
                st.error(f"❌ Failed to parse prediction log: {e}")
        else:
            st.info("ℹ️ No prediction log available yet.")
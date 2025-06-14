# Athena Threat Detection

A real-time machine learning-based threat detection system designed to classify incoming network data and detect potential DDoS attacks. Built using Python, Flask, Streamlit, and a Random Forest classifier.

---

## 📌 Features

* Upload CSV files with 78 network traffic features for real-time prediction.
* Scalable Flask API serving a trained ML model.
* Interactive Streamlit dashboard for visualizing prediction results.
* Logging system for timestamped prediction records.
* Integrated alert logging for detected DDoS threats.

---

## 🚀 How It Works

### 1. **Data Input**

Upload a CSV file with 78 features per row (matching the CICIDS2017 dataset format).

### 2. **Model Inference (Flask API)**

* API accepts POST requests with feature data.
* Features are scaled and passed into the trained Random Forest model.
* Model returns `0` for benign and `-1` for DDoS.

### 3. **Dashboard (Streamlit)**

* Visualizes prediction results.
* Saves prediction logs with timestamps.
* Plots:

  * Bar chart of prediction counts
  * Time series chart of predictions over time

### 4. **Alert System**

* Whenever a `-1` (DDoS) is predicted, an alert is logged in a dedicated file.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Flask** for backend API
* **Streamlit** for dashboard
* **Scikit-learn** for ML
* **Pandas/Numpy** for data processing
* **Matplotlib + Seaborn** for visualization

---

## 🧪 Folder Structure

```
athena-threat-detection/
├── dashboard/               # Streamlit dashboard code
│   └── dashboard.py
├── model_training/         # Model training scripts
│   └── train_model.py
├── models/                 # Saved ML models
│   ├── best_random_forest_model.pkl
│   └── scaler.pkl
├── app/                    # Flask API
│   └── app.py
├── logs/                   # Prediction logs
│   └── prediction_log.csv
├── alerts/                 # Alert logs
│   └── alerts_log.txt
├── data/                   # Sample and processed data
│   └── sample_real_inputs.csv
└── README.md               # Project overview
```

---

## 🖥️ Setup Instructions

### 🔧 Step 1: Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/athena-threat-detection.git
cd athena-threat-detection
```

### 🔧 Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 🔧 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔧 Step 4: Start Flask API

```bash
cd api
python app.py
```

### 🔧 Step 5: Launch Dashboard

In another terminal window:

```bash
cd dashboard
streamlit run dashboard.py
```

---

## 📊 Input Format

Each input should contain **78 numerical features** derived from network traffic data. Data used is based on [CICIDS2017 - DDoS subset](https://www.unb.ca/cic/datasets/ids-2017.html).

Example row:

```
80.0, 8076283.0, 8.0, 4.0, 56.0, 11607.0, 20.0, 0.0, ... , 24977.0, -1
```

---

## 📈 Enhancements in Progress

* [x] Scaled inputs with StandardScaler
* [x] Timestamped prediction logs
* [x] Alerting mechanism for DDoS
* [x] Interactive dashboard
* [ ] Integration with attack simulator (Scapy + Locust)
* [ ] Authentication for API access

---

## 🤖 Model Info

* **Algorithm**: Random Forest
* **Dataset**: CICIDS2017 (DDoS traffic on Friday Working Hours)
* **Accuracy**: \~99% on test set

---

## 🛡️ Future Goals

* Add attack simulator as a separate module (Scapy/Locust)
* Deploy model to cloud (Render / Heroku / GCP)
* Add real packet capture parser (e.g., using pyshark)
* Export logs to SIEM-compatible formats (e.g., JSON, Syslog)

---

## 👨‍💻 Author

Haripriya Arya
Cybersecurity Enthusiast | Penetration Tester

---

## ⭐ GitHub Project Page

Visit: [https://github.com/haripriya7112000/athena-threat-detection](https://github.com/haripriya7112000/athena-threat-detection)

---

## 📌 License

MIT License - feel free to use, enhance, and share!

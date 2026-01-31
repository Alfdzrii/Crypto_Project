# 🛡️ IDS Machine Learning Dashboard

A comprehensive **Intrusion Detection System (IDS)** with Machine Learning capabilities, featuring a modern cybersecurity dashboard with semi real-time monitoring and threat detection.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-green) ![ML](https://img.shields.io/badge/ML-Random%20Forest-orange)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🤖 Machine Learning
- **Random Forest Classifier** with 98%+ accuracy
- Trained on 10,000+ synthetic network traffic samples
- Detects multiple attack types: DoS, DDoS, Port Scan, Brute Force
- Offline learning model for stability and consistency

### 📊 Real-time Dashboard
- **Live monitoring** with auto-refresh every 3 seconds
- Interactive charts using Chart.js
- Real-time statistics and metrics
- Modern, responsive UI with glassmorphism design

### 🔄 Semi Real-time Detection
- Background service monitors traffic continuously
- Automatic threat classification
- Instant alerts for detected attacks
- Persistent logging to SQLite database

### 📡 Wireshark Integration
- Convert real packet captures to IDS format
- Analyze actual network traffic
- Merge normal and attack datasets
- Retrain model with real-world data

### 🎨 Modern UI/UX
- Premium gradient color scheme
- Smooth animations and transitions
- Professional SVG icons
- Responsive design for all screen sizes

### 📈 Advanced Analytics
- Traffic distribution visualization
- Detection rate monitoring
- Historical log analysis
- Threat type categorization

---

## 🎬 Demo

### Dashboard Interface
The dashboard provides a comprehensive view of network security status:

- **Status Indicator**: Real-time security status (Safe/Warning/Danger)
- **Statistics Cards**: Total packets, detected attacks, detection rate
- **Traffic Chart**: Visual distribution of normal vs attack traffic
- **Detection Logs**: Detailed history of all analyzed packets
- **Control Panel**: Start/stop monitoring, upload CSV files

### Key Metrics

| Metric | Description | Typical Value |
|--------|-------------|---------------|
| **Total Packets** | Number of analyzed network packets | 0 - ∞ |
| **Detected Attacks** | Number of threats identified | 0 - ∞ |
| **Detection Rate** | Percentage of attack traffic | 0% - 100% |
| **Model Accuracy** | ML model performance | 98%+ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Dashboard (UI)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Status  │  │  Charts  │  │   Logs   │  │ Control │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↕ AJAX/REST API
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend Server                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ API Endpoints│  │  Monitoring  │  │  File Upload  │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────┐
│              Machine Learning Pipeline                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ Preprocessor │→ │Random Forest │→ │  Prediction   │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │SQLite Database│  │Training Data │  │ Stream Data   │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Flask (Python)
- **ML Framework**: scikit-learn
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Data Processing**: pandas, numpy

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "CRYPTO FINAL"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask
- pandas
- scikit-learn
- numpy

### Step 3: Generate Training Data

```bash
python data/generator.py --generate-training --samples 10000
```

This creates `training_data.csv` with 10,000 samples (70% normal, 30% attack).

### Step 4: Train ML Model

```bash
python models/ml_model.py
```

This trains the Random Forest model and saves it as `trained_model.pkl`.

---

## ⚡ Quick Start

### Basic Usage

```bash
# 1. Start the Flask server
python app.py

# 2. Open browser
http://localhost:5000

# 3. Start monitoring
Click "Start Monitoring" button

# 4. (Optional) Simulate traffic
# In a new terminal:
python data/generator.py --simulate-stream
```

### Upload CSV File

```bash
# 1. Prepare CSV file in IDS format
# Use training_data.csv as template

# 2. Click "Upload CSV" on dashboard

# 3. Select file and upload

# 4. View analysis results
```

---

## 📖 Usage Guide

### 1. Real-time Monitoring

**Start Monitoring:**
```
1. Click "Start Monitoring" button
2. Status changes to "Monitoring: Running"
3. Dashboard auto-updates every 3 seconds
```

**Simulate Traffic:**
```bash
python data/generator.py --simulate-stream --interval 3
```

**Stop Monitoring:**
```
1. Click "Stop Monitoring" button
2. Status changes to "Monitoring: Stopped"
```

### 2. Batch Analysis (Upload CSV)

**Prepare CSV File:**
```csv
duration,protocol_type,service,flag,src_bytes,dst_bytes,...
0.5,tcp,http,SF,429,2966,...
1.2,tcp,smtp,S0,512,1024,...
```

**Upload:**
```
1. Click "Upload CSV" button
2. Select file
3. Wait for processing
4. View results in dashboard
```

### 3. Wireshark Integration

**Capture Traffic:**
```
1. Open Wireshark
2. Select network interface
3. Start capture
4. Stop after collecting data
5. Export as CSV
```

**Convert to IDS Format:**
```bash
python data/wireshark_converter.py \
    --wireshark-csv capture.csv \
    --output ids_data.csv \
    --label normal
```

**Upload to Dashboard:**
```
1. Use converted ids_data.csv
2. Upload via dashboard
3. Analyze results
```

### 4. Retrain Model

**With New Data:**
```bash
# 1. Prepare new training data
# Merge with existing: training_data.csv

# 2. Retrain model
python models/ml_model.py

# 3. Restart server
python app.py
```

---

## 📁 Project Structure

```
CRYPTO FINAL/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── data/                       # Data files
│   ├── generator.py           # Synthetic data generator
│   ├── wireshark_converter.py # Wireshark CSV converter
│   ├── training_data.csv      # Training dataset (10K samples)
│   ├── stream_data.csv        # Real-time stream data
│   ├── sample_upload.csv      # Sample upload file
│   └── diverse_traffic_5000.csv # Additional dataset
│
├── models/                     # Machine Learning models
│   ├── ml_model.py            # Random Forest model
│   ├── trained_model.pkl      # Saved model
│   └── scaler.pkl             # Feature scaler
│
├── services/                   # Backend services
│   ├── monitoring.py          # Background monitoring service
│   └── preprocessor.py        # Data preprocessing
│
├── database/                   # Database layer
│   ├── models.py              # Database models
│   ├── db_manager.py          # Database operations
│   └── ids_logs.db            # SQLite database
│
├── templates/                  # HTML templates
│   └── dashboard.html         # Main dashboard
│
├── static/                     # Static assets
│   ├── css/
│   │   └── dashboard.css      # Dashboard styles
│   └── js/
│       ├── dashboard.js       # Dashboard logic
│       └── charts.js          # Chart configurations
│
└── docs/                       # Documentation
    ├── QUICK_START.md         # Quick start guide (ID)
    ├── TROUBLESHOOTING.md     # Common issues
    ├── WIRESHARK_GUIDE.md     # Wireshark integration
    ├── DATA_GENERATION_GUIDE.md # Data generation
    ├── TRAINING_DATA_EXPLAINED.md # Training data info
    └── UI_MODERNIZATION.md    # UI design changes
```

---

## 📚 Documentation

### Available Guides

1. **[QUICK_START.md](QUICK_START.md)** - Panduan cepat (Bahasa Indonesia)
2. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solusi masalah umum
3. **[WIRESHARK_GUIDE.md](WIRESHARK_GUIDE.md)** - Integrasi Wireshark
4. **[DATA_GENERATION_GUIDE.md](DATA_GENERATION_GUIDE.md)** - Generate data
5. **[TRAINING_DATA_EXPLAINED.md](TRAINING_DATA_EXPLAINED.md)** - Penjelasan data training
6. **[UI_MODERNIZATION.md](UI_MODERNIZATION.md)** - Perubahan UI design

### Key Concepts

**Detection Rate:**
- Percentage of attack traffic detected
- Formula: `(Detected Attacks / Total Packets) × 100%`
- Typical range: 0% (safe) to 100% (under attack)

**Monitoring Service:**
- Background thread running every 3 seconds
- Reads `stream_data.csv` for new traffic
- Automatically classifies and logs results

**ML Model:**
- Random Forest with 100 estimators
- Trained on 29 features
- Offline learning (no online updates)
- 98%+ accuracy on test data

---

## 🔧 Troubleshooting

### Common Issues

**1. Model Not Loading**
```bash
# Solution: Retrain model
python models/ml_model.py
```

**2. Upload CSV Fails**
```
Error: Missing required columns

Solution:
- Use training_data.csv as template
- Ensure all 29 columns are present
- Check column names match exactly
```

**3. Monitoring Not Working**
```bash
# Solution: Check stream_data.csv exists
python data/generator.py --simulate-stream
```

**4. Port Already in Use**
```bash
# Solution: Change port in config.py
# Or kill existing process:
taskkill /F /IM python.exe
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎓 Academic Use

This project is designed as an **academic prototype** for learning and demonstration purposes.

### Suitable For:
- ✅ Final year projects
- ✅ Machine learning coursework
- ✅ Cybersecurity demonstrations
- ✅ Network security research
- ✅ IDS concept learning

### Limitations:
- ⚠️ Uses synthetic data (not production-ready)
- ⚠️ Simplified feature set
- ⚠️ No real-time packet capture
- ⚠️ Single-user application
- ⚠️ Limited attack types

### Presentation Tips:
1. Start with monitoring demo
2. Show real-time detection
3. Upload CSV with attacks
4. Explain ML model accuracy
5. Demonstrate Wireshark integration

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is created for academic purposes. Feel free to use and modify for educational projects.

---

## 👥 Authors

- **Your Name** - Initial work and development

---

## 🙏 Acknowledgments

- scikit-learn for ML framework
- Flask for web framework
- Chart.js for visualizations
- Wireshark for packet capture inspiration

---

## 📞 Support

For questions or issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review documentation in `/docs`
3. Open an issue on GitHub

---

## 🔄 Version History

- **v1.0** (2026-01-31)
  - Initial release
  - Random Forest ML model
  - Real-time monitoring
  - Wireshark integration
  - Modern UI design
  - Complete documentation

---

**Made with ❤️ for Cybersecurity Education**

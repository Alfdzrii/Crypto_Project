"""
Configuration settings for IDS Machine Learning Application
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'ids_logs.db')

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, 'models')
TRAINED_MODEL_PATH = os.path.join(MODEL_DIR, 'trained_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

# Data paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
TRAINING_DATA_PATH = os.path.join(DATA_DIR, 'training_data.csv')
STREAM_DATA_PATH = os.path.join(DATA_DIR, 'stream_data.csv')

# Monitoring configuration
MONITORING_INTERVAL = 3  # seconds
STREAM_CHECK_INTERVAL = 3  # seconds

# Alert thresholds
SAFE_THRESHOLD = 0.1  # < 10% attacks = SAFE
WARNING_THRESHOLD = 0.3  # 10-30% attacks = WARNING
# > 30% attacks = DANGER

# Application settings
SECRET_KEY = 'ids-ml-secret-key-change-in-production'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Feature columns for ML model
FEATURE_COLUMNS = [
    'duration',
    'protocol_type',
    'service',
    'flag',
    'src_bytes',
    'dst_bytes',
    'land',
    'wrong_fragment',
    'urgent',
    'hot',
    'num_failed_logins',
    'logged_in',
    'num_compromised',
    'root_shell',
    'su_attempted',
    'num_root',
    'num_file_creations',
    'num_shells',
    'num_access_files',
    'count',
    'srv_count',
    'serror_rate',
    'srv_serror_rate',
    'rerror_rate',
    'srv_rerror_rate',
    'same_srv_rate',
    'diff_srv_rate',
    'srv_diff_host_rate'
]

# Categorical columns that need encoding
CATEGORICAL_COLUMNS = ['protocol_type', 'service', 'flag']

"""
Flask Application for IDS Machine Learning Dashboard
Main entry point for the web application
"""
from flask import Flask, render_template, jsonify, request
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from database.models import get_database
from models.ml_model import load_trained_model
from services.monitoring import get_monitoring_service

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Initialize components
print("\n" + "=" * 60)
print("INITIALIZING IDS MACHINE LEARNING APPLICATION")
print("=" * 60)

# Initialize database
database = get_database(config.DATABASE_PATH)

# Load ML model
try:
    model = load_trained_model()
    print("✓ ML model loaded successfully")
except FileNotFoundError:
    print("⚠ ML model not found. Please train the model first.")
    print("  Run: python models/ml_model.py")
    model = None

# Initialize monitoring service
if model:
    monitoring_service = get_monitoring_service(model, database)
else:
    monitoring_service = None

print("=" * 60 + "\n")


@app.route('/')
def dashboard():
    """Render main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/status')
def api_status():
    """Get current system status and statistics"""
    if not monitoring_service:
        return jsonify({'error': 'Monitoring service not available'}), 503
    
    # Get statistics from database
    db_stats = database.get_statistics()
    
    # Get traffic distribution
    distribution = database.get_traffic_distribution()
    
    # Get monitoring service stats
    service_stats = monitoring_service.get_stats()
    
    return jsonify({
        'status': service_stats['status'],
        'monitoring_active': monitoring_service.is_running(),
        'total_packets': db_stats['total_packets'],
        'total_attacks': db_stats['total_attacks'],
        'detection_rate': db_stats['detection_rate'],
        'last_threat': db_stats['last_threat'],
        'distribution': distribution
    })


@app.route('/api/logs')
def api_logs():
    """Get recent detection logs"""
    limit = request.args.get('limit', 20, type=int)
    logs = database.get_recent_logs(limit=limit)
    
    return jsonify({
        'logs': logs,
        'count': len(logs)
    })


@app.route('/api/control', methods=['POST'])
def api_control():
    """Control monitoring service (start/stop)"""
    if not monitoring_service:
        return jsonify({'error': 'Monitoring service not available'}), 503
    
    data = request.get_json()
    action = data.get('action')
    
    if action == 'start':
        success = monitoring_service.start()
        return jsonify({
            'success': success,
            'message': 'Monitoring started' if success else 'Already running'
        })
    
    elif action == 'stop':
        success = monitoring_service.stop()
        return jsonify({
            'success': success,
            'message': 'Monitoring stopped' if success else 'Not running'
        })
    
    else:
        return jsonify({'error': 'Invalid action'}), 400


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Upload and analyze batch traffic data"""
    if not model:
        return jsonify({'error': 'ML model not available'}), 503
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400
    
    try:
        # Read CSV file
        import pandas as pd
        df = pd.read_csv(file)
        
        # Check if file has required columns
        required_columns = config.FEATURE_COLUMNS
        missing_columns = [col for col in required_columns if col not in df.columns and col != 'label']
        
        # If missing columns, provide helpful error
        if missing_columns:
            return jsonify({
                'error': f'CSV file is missing required columns. Please use training_data.csv as template.',
                'missing_columns': missing_columns[:5],  # Show first 5 missing columns
                'hint': 'Upload a CSV file with the same format as training_data.csv'
            }), 400
        
        # Process each row
        results = {
            'total': len(df),
            'normal': 0,
            'attack': 0,
            'processed': 0
        }
        
        for idx, row in df.iterrows():
            try:
                features = row.to_dict()
                
                # Remove label if present
                if 'label' in features:
                    del features['label']
                
                # Predict
                result = model.predict(features)
                
                # Save to database
                threat_type = None
                if result['prediction'] == 'attack':
                    threat_type = 'Batch Upload'
                    results['attack'] += 1
                else:
                    results['normal'] += 1
                
                database.insert_log(
                    prediction=result['prediction'],
                    confidence=result['confidence'],
                    features=features,
                    threat_type=threat_type
                )
                
                results['processed'] += 1
                
            except Exception as row_error:
                print(f"Error processing row {idx}: {row_error}")
                continue
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Upload error: {error_detail}")
        return jsonify({
            'error': 'Failed to process CSV file. Please ensure it has the correct format.',
            'detail': str(e)
        }), 500


@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'database_connected': database is not None,
        'monitoring_available': monitoring_service is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("STARTING IDS DASHBOARD SERVER")
    print("=" * 60)
    print(f"Server: http://{config.HOST}:{config.PORT}")
    print(f"Dashboard: http://localhost:{config.PORT}")
    print("=" * 60 + "\n")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )

"""
Background monitoring service for real-time traffic analysis
Reads stream data, runs ML predictions, and saves to database
"""
import threading
import time
import os
import pandas as pd
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from database.models import get_database
from models.ml_model import load_trained_model


class MonitoringService:
    """Background service for monitoring network traffic stream"""
    
    def __init__(self, model, database):
        self.model = model
        self.database = database
        self.running = False
        self.thread = None
        self.last_position = 0
        self.lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'total_packets': 0,
            'total_attacks': 0,
            'last_threat': None,
            'status': 'SAFE'
        }
    
    def start(self):
        """Start the monitoring service"""
        if self.running:
            print("⚠ Monitoring service is already running")
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("✓ Monitoring service started")
        return True
    
    def stop(self):
        """Stop the monitoring service"""
        if not self.running:
            print("⚠ Monitoring service is not running")
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✓ Monitoring service stopped")
        return True
    
    def _monitor_loop(self):
        """Main monitoring loop (runs in background thread)"""
        print(f"Monitoring stream file: {config.STREAM_DATA_PATH}")
        
        # Initialize stream file position
        if os.path.exists(config.STREAM_DATA_PATH):
            # Count existing lines to set initial position
            with open(config.STREAM_DATA_PATH, 'r') as f:
                self.last_position = sum(1 for _ in f) - 1  # -1 for header
                print(f"Starting from position: {self.last_position}")
        else:
            print("⚠ Stream file not found, waiting for data...")
        
        while self.running:
            try:
                # Check for new data
                new_data = self._read_new_data()
                
                if new_data is not None and len(new_data) > 0:
                    # Process each new traffic instance
                    for idx, row in new_data.iterrows():
                        self._process_traffic(row.to_dict())
                    
                    # Update statistics
                    self._update_stats()
                
                # Wait before next check
                time.sleep(config.STREAM_CHECK_INTERVAL)
                
            except Exception as e:
                print(f"⚠ Error in monitoring loop: {e}")
                time.sleep(config.STREAM_CHECK_INTERVAL)
    
    def _read_new_data(self):
        """Read new lines from stream file"""
        if not os.path.exists(config.STREAM_DATA_PATH):
            return None
        
        try:
            # Read entire file
            df = pd.read_csv(config.STREAM_DATA_PATH)
            
            # Get new rows since last position
            if len(df) > self.last_position:
                new_data = df.iloc[self.last_position:]
                self.last_position = len(df)
                return new_data
            
            return None
            
        except Exception as e:
            print(f"⚠ Error reading stream file: {e}")
            return None
    
    def _process_traffic(self, features):
        """Process a single traffic instance"""
        try:
            # Remove label if present (for stream data)
            if 'label' in features:
                del features['label']
            
            # Run ML prediction
            result = self.model.predict(features)
            
            # Determine threat type if attack
            threat_type = None
            if result['prediction'] == 'attack':
                threat_type = self._classify_threat(features)
            
            # Save to database
            with self.lock:
                self.database.insert_log(
                    prediction=result['prediction'],
                    confidence=result['confidence'],
                    features=features,
                    threat_type=threat_type
                )
            
            # Log detection
            timestamp = datetime.now().strftime('%H:%M:%S')
            if result['prediction'] == 'attack':
                print(f"[{timestamp}] 🚨 ATTACK DETECTED - {threat_type} (confidence: {result['confidence']:.2%})")
            else:
                print(f"[{timestamp}] ✓ Normal traffic (confidence: {result['confidence']:.2%})")
            
        except Exception as e:
            print(f"⚠ Error processing traffic: {e}")
    
    def _classify_threat(self, features):
        """Classify the type of attack based on features"""
        # Simple heuristic-based threat classification
        
        # DoS/DDoS - high connection count, low duration
        if features.get('count', 0) > 200 and features.get('duration', 0) < 1:
            if features.get('srv_diff_host_rate', 0) > 0.5:
                return 'DDoS'
            return 'DoS'
        
        # Port Scan - many different services, high error rate
        if features.get('diff_srv_rate', 0) > 0.5 and features.get('serror_rate', 0) > 0.5:
            return 'Port Scan'
        
        # Brute Force - failed logins
        if features.get('num_failed_logins', 0) > 0:
            return 'Brute Force'
        
        # Default
        return 'Unknown Attack'
    
    def _update_stats(self):
        """Update statistics from database"""
        with self.lock:
            db_stats = self.database.get_statistics()
            self.stats['total_packets'] = db_stats['total_packets']
            self.stats['total_attacks'] = db_stats['total_attacks']
            self.stats['last_threat'] = db_stats['last_threat']
            
            # Update status based on attack ratio
            if self.stats['total_packets'] > 0:
                attack_ratio = self.stats['total_attacks'] / self.stats['total_packets']
                
                if attack_ratio < config.SAFE_THRESHOLD:
                    self.stats['status'] = 'SAFE'
                elif attack_ratio < config.WARNING_THRESHOLD:
                    self.stats['status'] = 'WARNING'
                else:
                    self.stats['status'] = 'DANGER'
    
    def get_stats(self):
        """Get current statistics (thread-safe)"""
        with self.lock:
            return self.stats.copy()
    
    def is_running(self):
        """Check if service is running"""
        return self.running


# Global monitoring service instance
_monitoring_service = None


def get_monitoring_service(model, database):
    """Get or create monitoring service singleton"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService(model, database)
    return _monitoring_service

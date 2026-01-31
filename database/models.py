"""
Database models and operations for IDS logging
"""
import sqlite3
import json
from datetime import datetime
import os


class Database:
    """SQLite database handler for IDS detection logs"""
    
    def __init__(self, db_path):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create database tables if they don't exist"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create detection_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                threat_type TEXT,
                features_json TEXT,
                src_bytes INTEGER,
                dst_bytes INTEGER,
                protocol_type TEXT,
                service TEXT,
                flag TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Database initialized: {self.db_path}")
    
    def insert_log(self, prediction, confidence, features, threat_type=None):
        """
        Insert a new detection log
        
        Args:
            prediction: 'normal' or 'attack'
            confidence: Prediction confidence (0-1)
            features: Dictionary of traffic features
            threat_type: Type of threat if attack detected
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Extract key features for quick access
        src_bytes = features.get('src_bytes', 0)
        dst_bytes = features.get('dst_bytes', 0)
        protocol_type = features.get('protocol_type', '')
        service = features.get('service', '')
        flag = features.get('flag', '')
        
        cursor.execute('''
            INSERT INTO detection_logs 
            (prediction, confidence, threat_type, features_json, 
             src_bytes, dst_bytes, protocol_type, service, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            prediction,
            confidence,
            threat_type,
            json.dumps(features),
            src_bytes,
            dst_bytes,
            protocol_type,
            service,
            flag
        ))
        
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        
        return log_id
    
    def get_recent_logs(self, limit=20):
        """Get most recent detection logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, prediction, confidence, threat_type,
                   src_bytes, dst_bytes, protocol_type, service, flag
            FROM detection_logs
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'id': row[0],
                'timestamp': row[1],
                'prediction': row[2],
                'confidence': row[3],
                'threat_type': row[4],
                'src_bytes': row[5],
                'dst_bytes': row[6],
                'protocol_type': row[7],
                'service': row[8],
                'flag': row[9]
            })
        
        return logs
    
    def get_statistics(self):
        """Get overall detection statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total packets analyzed
        cursor.execute('SELECT COUNT(*) FROM detection_logs')
        total_packets = cursor.fetchone()[0]
        
        # Total attacks detected
        cursor.execute("SELECT COUNT(*) FROM detection_logs WHERE prediction = 'attack'")
        total_attacks = cursor.fetchone()[0]
        
        # Get last detected threat
        cursor.execute('''
            SELECT timestamp, threat_type, confidence, protocol_type, service
            FROM detection_logs
            WHERE prediction = 'attack'
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        
        last_threat_row = cursor.fetchone()
        last_threat = None
        
        if last_threat_row:
            last_threat = {
                'timestamp': last_threat_row[0],
                'threat_type': last_threat_row[1],
                'confidence': last_threat_row[2],
                'protocol': last_threat_row[3],
                'service': last_threat_row[4]
            }
        
        conn.close()
        
        # Calculate detection rate
        detection_rate = (total_attacks / total_packets * 100) if total_packets > 0 else 0
        
        return {
            'total_packets': total_packets,
            'total_attacks': total_attacks,
            'detection_rate': round(detection_rate, 2),
            'last_threat': last_threat
        }
    
    def get_traffic_distribution(self):
        """Get distribution of normal vs attack traffic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT prediction, COUNT(*) as count
            FROM detection_logs
            GROUP BY prediction
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        distribution = {'normal': 0, 'attack': 0}
        for row in rows:
            distribution[row[0]] = row[1]
        
        return distribution
    
    def clear_logs(self):
        """Clear all detection logs (for testing)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM detection_logs')
        conn.commit()
        conn.close()
        print("✓ All logs cleared")


# Singleton database instance
_db_instance = None


def get_database(db_path):
    """Get or create database singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(db_path)
    return _db_instance

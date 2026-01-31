"""
Network Traffic Data Generator for IDS Training and Simulation
Generates synthetic network traffic data with both normal and attack patterns
"""
import pandas as pd
import numpy as np
import random
import time
import os
from datetime import datetime

# Attack types and their characteristics
ATTACK_TYPES = ['DoS', 'Port Scan', 'DDoS', 'Brute Force']
PROTOCOLS = ['tcp', 'udp', 'icmp']
SERVICES = ['http', 'ftp', 'smtp', 'ssh', 'dns', 'telnet', 'private']
FLAGS = ['SF', 'S0', 'REJ', 'RSTR', 'SH', 'S1', 'S2', 'S3']


def generate_normal_traffic():
    """Generate a single normal traffic record"""
    return {
        'duration': np.random.exponential(10),
        'protocol_type': random.choice(['tcp', 'udp']),
        'service': random.choice(['http', 'ftp', 'smtp', 'dns']),
        'flag': random.choice(['SF', 'S0']),
        'src_bytes': np.random.randint(50, 5000),
        'dst_bytes': np.random.randint(50, 5000),
        'land': 0,
        'wrong_fragment': 0,
        'urgent': 0,
        'hot': np.random.randint(0, 3),
        'num_failed_logins': 0,
        'logged_in': 1,
        'num_compromised': 0,
        'root_shell': 0,
        'su_attempted': 0,
        'num_root': 0,
        'num_file_creations': np.random.randint(0, 3),
        'num_shells': 0,
        'num_access_files': np.random.randint(0, 2),
        'count': np.random.randint(1, 100),
        'srv_count': np.random.randint(1, 100),
        'serror_rate': np.random.uniform(0, 0.1),
        'srv_serror_rate': np.random.uniform(0, 0.1),
        'rerror_rate': np.random.uniform(0, 0.1),
        'srv_rerror_rate': np.random.uniform(0, 0.1),
        'same_srv_rate': np.random.uniform(0.8, 1.0),
        'diff_srv_rate': np.random.uniform(0, 0.2),
        'srv_diff_host_rate': np.random.uniform(0, 0.2),
        'label': 'normal'
    }


def generate_attack_traffic():
    """Generate a single attack traffic record"""
    attack_type = random.choice(ATTACK_TYPES)
    
    if attack_type == 'DoS':
        # Denial of Service characteristics
        return {
            'duration': 0,
            'protocol_type': 'tcp',
            'service': random.choice(['http', 'private']),
            'flag': random.choice(['S0', 'REJ', 'RSTR']),
            'src_bytes': 0,
            'dst_bytes': 0,
            'land': random.choice([0, 1]),
            'wrong_fragment': np.random.randint(0, 3),
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'count': np.random.randint(200, 500),
            'srv_count': np.random.randint(200, 500),
            'serror_rate': np.random.uniform(0.9, 1.0),
            'srv_serror_rate': np.random.uniform(0.9, 1.0),
            'rerror_rate': 0,
            'srv_rerror_rate': 0,
            'same_srv_rate': np.random.uniform(0.9, 1.0),
            'diff_srv_rate': np.random.uniform(0, 0.1),
            'srv_diff_host_rate': 0,
            'label': 'attack'
        }
    
    elif attack_type == 'Port Scan':
        # Port scanning characteristics
        return {
            'duration': 0,
            'protocol_type': random.choice(['tcp', 'icmp']),
            'service': 'private',
            'flag': random.choice(['S0', 'REJ', 'RSTR']),
            'src_bytes': np.random.randint(0, 100),
            'dst_bytes': 0,
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'count': np.random.randint(100, 300),
            'srv_count': np.random.randint(1, 10),
            'serror_rate': np.random.uniform(0.5, 1.0),
            'srv_serror_rate': np.random.uniform(0, 0.5),
            'rerror_rate': np.random.uniform(0.5, 1.0),
            'srv_rerror_rate': 0,
            'same_srv_rate': np.random.uniform(0, 0.2),
            'diff_srv_rate': np.random.uniform(0.8, 1.0),
            'srv_diff_host_rate': np.random.uniform(0, 0.3),
            'label': 'attack'
        }
    
    elif attack_type == 'DDoS':
        # Distributed Denial of Service
        return {
            'duration': 0,
            'protocol_type': random.choice(['tcp', 'udp']),
            'service': random.choice(['http', 'dns']),
            'flag': 'S0',
            'src_bytes': np.random.randint(0, 200),
            'dst_bytes': 0,
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'count': np.random.randint(300, 600),
            'srv_count': np.random.randint(300, 600),
            'serror_rate': np.random.uniform(0.8, 1.0),
            'srv_serror_rate': np.random.uniform(0.8, 1.0),
            'rerror_rate': 0,
            'srv_rerror_rate': 0,
            'same_srv_rate': np.random.uniform(0.9, 1.0),
            'diff_srv_rate': np.random.uniform(0, 0.1),
            'srv_diff_host_rate': np.random.uniform(0.8, 1.0),
            'label': 'attack'
        }
    
    else:  # Brute Force
        return {
            'duration': np.random.uniform(0, 5),
            'protocol_type': 'tcp',
            'service': random.choice(['ftp', 'ssh', 'telnet']),
            'flag': random.choice(['SF', 'S0', 'REJ']),
            'src_bytes': np.random.randint(50, 500),
            'dst_bytes': np.random.randint(0, 100),
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': np.random.randint(0, 5),
            'num_failed_logins': np.random.randint(1, 10),
            'logged_in': 0,
            'num_compromised': np.random.randint(0, 3),
            'root_shell': 0,
            'su_attempted': np.random.randint(0, 2),
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'count': np.random.randint(50, 150),
            'srv_count': np.random.randint(50, 150),
            'serror_rate': np.random.uniform(0, 0.3),
            'srv_serror_rate': np.random.uniform(0, 0.3),
            'rerror_rate': np.random.uniform(0.3, 0.8),
            'srv_rerror_rate': np.random.uniform(0.3, 0.8),
            'same_srv_rate': np.random.uniform(0.5, 0.9),
            'diff_srv_rate': np.random.uniform(0.1, 0.5),
            'srv_diff_host_rate': np.random.uniform(0, 0.3),
            'label': 'attack'
        }


def generate_training_data(num_samples=10000, output_path='training_data.csv'):
    """
    Generate training dataset with balanced normal and attack traffic
    
    Args:
        num_samples: Total number of samples to generate
        output_path: Path to save the CSV file
    """
    print(f"Generating {num_samples} training samples...")
    
    data = []
    num_normal = int(num_samples * 0.7)  # 70% normal traffic
    num_attack = num_samples - num_normal  # 30% attack traffic
    
    # Generate normal traffic
    for i in range(num_normal):
        data.append(generate_normal_traffic())
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1} normal samples...")
    
    # Generate attack traffic
    for i in range(num_attack):
        data.append(generate_attack_traffic())
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1} attack samples...")
    
    # Create DataFrame and shuffle
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✓ Training data saved to {output_path}")
    print(f"  Normal: {num_normal} samples")
    print(f"  Attack: {num_attack} samples")
    print(f"  Total: {num_samples} samples")
    
    return df


def simulate_stream(output_path='stream_data.csv', interval=3, duration=None):
    """
    Simulate real-time network traffic stream by appending data to CSV
    
    Args:
        output_path: Path to the stream CSV file
        interval: Seconds between each batch of new data
        duration: Total duration in seconds (None = infinite)
    """
    print(f"Starting traffic stream simulation...")
    print(f"  Output: {output_path}")
    print(f"  Interval: {interval} seconds")
    print(f"  Duration: {'Infinite' if duration is None else f'{duration} seconds'}")
    print("  Press Ctrl+C to stop\n")
    
    # Initialize stream file with headers if it doesn't exist
    if not os.path.exists(output_path):
        sample = generate_normal_traffic()
        df = pd.DataFrame([sample])
        df.to_csv(output_path, index=False)
        print(f"✓ Initialized stream file: {output_path}\n")
    
    start_time = time.time()
    batch_count = 0
    
    try:
        while True:
            # Check duration limit
            if duration and (time.time() - start_time) >= duration:
                print("\n✓ Stream simulation completed (duration limit reached)")
                break
            
            # Generate batch of new traffic (1-5 packets per batch)
            batch_size = random.randint(1, 5)
            new_data = []
            
            for _ in range(batch_size):
                # 70% normal, 30% attack
                if random.random() < 0.7:
                    new_data.append(generate_normal_traffic())
                else:
                    new_data.append(generate_attack_traffic())
            
            # Append to stream file
            df_new = pd.DataFrame(new_data)
            df_new.to_csv(output_path, mode='a', header=False, index=False)
            
            batch_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Batch #{batch_count}: Added {batch_size} packets to stream")
            
            # Wait for next batch
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✓ Stream simulation stopped by user")
        print(f"  Total batches generated: {batch_count}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Network Traffic Data Generator')
    parser.add_argument('--generate-training', action='store_true',
                        help='Generate training dataset')
    parser.add_argument('--samples', type=int, default=10000,
                        help='Number of training samples (default: 10000)')
    parser.add_argument('--simulate-stream', action='store_true',
                        help='Simulate real-time traffic stream')
    parser.add_argument('--interval', type=int, default=3,
                        help='Stream interval in seconds (default: 3)')
    parser.add_argument('--duration', type=int, default=None,
                        help='Stream duration in seconds (default: infinite)')
    
    args = parser.parse_args()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.generate_training:
        output_path = os.path.join(script_dir, 'training_data.csv')
        generate_training_data(num_samples=args.samples, output_path=output_path)
    
    elif args.simulate_stream:
        output_path = os.path.join(script_dir, 'stream_data.csv')
        simulate_stream(output_path=output_path, interval=args.interval, duration=args.duration)
    
    else:
        parser.print_help()

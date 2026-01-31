"""
Wireshark Data Converter for IDS System
Converts Wireshark packet captures to IDS-compatible format
"""
import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime


# Wireshark to IDS feature mapping
WIRESHARK_FEATURE_MAP = {
    # Basic packet info
    'frame.time_relative': 'duration',
    'ip.proto': 'protocol_type',
    'tcp.dstport': 'service',
    'tcp.flags': 'flag',
    'frame.len': 'src_bytes',
    'ip.len': 'dst_bytes',
    
    # TCP/IP features
    'tcp.analysis.retransmission': 'wrong_fragment',
    'tcp.urgent_pointer': 'urgent',
    'tcp.connection.syn': 'hot',
    
    # Connection features
    'tcp.analysis.ack_rtt': 'count',
    'tcp.stream': 'srv_count',
}


def protocol_number_to_name(proto_num):
    """Convert IP protocol number to name"""
    protocol_map = {
        1: 'icmp',
        6: 'tcp',
        17: 'udp',
    }
    return protocol_map.get(proto_num, 'other')


def port_to_service(port):
    """Convert port number to service name"""
    service_map = {
        20: 'ftp-data',
        21: 'ftp',
        22: 'ssh',
        23: 'telnet',
        25: 'smtp',
        53: 'dns',
        80: 'http',
        110: 'pop3',
        143: 'imap',
        443: 'https',
        3306: 'mysql',
        5432: 'postgresql',
    }
    
    if port is None or pd.isna(port):
        return 'private'
    
    port = int(port)
    return service_map.get(port, 'private')


def tcp_flags_to_flag(flags):
    """Convert TCP flags to connection flag"""
    if pd.isna(flags):
        return 'S0'
    
    flags = str(flags).upper()
    
    # Map common TCP flag combinations
    if 'SYN' in flags and 'ACK' not in flags:
        return 'S0'  # SYN only
    elif 'SYN' in flags and 'ACK' in flags:
        return 'S1'  # SYN-ACK
    elif 'FIN' in flags and 'ACK' in flags:
        return 'SF'  # Normal close
    elif 'RST' in flags:
        return 'REJ'  # Reset
    else:
        return 'S0'


def convert_wireshark_to_ids(wireshark_csv_path, output_path, label='normal'):
    """
    Convert Wireshark CSV export to IDS training format
    
    Args:
        wireshark_csv_path: Path to Wireshark CSV export
        output_path: Path to save converted data
        label: Label for this data ('normal' or 'attack')
    """
    print(f"\n{'='*60}")
    print("WIRESHARK TO IDS CONVERTER")
    print(f"{'='*60}\n")
    
    # Read Wireshark CSV
    print(f"1. Reading Wireshark CSV: {wireshark_csv_path}")
    try:
        df_wireshark = pd.read_csv(wireshark_csv_path)
        print(f"   ✓ Loaded {len(df_wireshark)} packets")
        print(f"   ✓ Columns: {len(df_wireshark.columns)}")
    except Exception as e:
        print(f"   ✗ Error reading file: {e}")
        return
    
    print(f"\n2. Converting to IDS format...")
    
    # Initialize IDS format DataFrame
    ids_data = []
    
    for idx, row in df_wireshark.iterrows():
        try:
            # Extract and convert features
            packet = {
                # Duration (time relative to start)
                'duration': row.get('frame.time_relative', 0) if pd.notna(row.get('frame.time_relative')) else 0,
                
                # Protocol
                'protocol_type': protocol_number_to_name(row.get('ip.proto', 6)),
                
                # Service (from destination port)
                'service': port_to_service(row.get('tcp.dstport', row.get('udp.dstport'))),
                
                # Connection flag
                'flag': tcp_flags_to_flag(row.get('tcp.flags')),
                
                # Bytes
                'src_bytes': int(row.get('frame.len', 0)) if pd.notna(row.get('frame.len')) else 0,
                'dst_bytes': int(row.get('ip.len', 0)) if pd.notna(row.get('ip.len')) else 0,
                
                # Binary features
                'land': 1 if row.get('ip.src') == row.get('ip.dst') else 0,
                'wrong_fragment': 1 if pd.notna(row.get('tcp.analysis.retransmission')) else 0,
                'urgent': 1 if pd.notna(row.get('tcp.urgent_pointer')) and row.get('tcp.urgent_pointer') > 0 else 0,
                
                # Connection features (estimated from packet data)
                'hot': 0,  # Would need deeper inspection
                'num_failed_logins': 0,  # Would need application layer analysis
                'logged_in': 0,  # Would need application layer analysis
                'num_compromised': 0,
                'root_shell': 0,
                'su_attempted': 0,
                'num_root': 0,
                'num_file_creations': 0,
                'num_shells': 0,
                'num_access_files': 0,
                
                # Traffic statistics (would need to calculate from multiple packets)
                'count': 1,  # Placeholder
                'srv_count': 1,  # Placeholder
                'serror_rate': 0.0,
                'srv_serror_rate': 0.0,
                'rerror_rate': 0.0,
                'srv_rerror_rate': 0.0,
                'same_srv_rate': 1.0,
                'diff_srv_rate': 0.0,
                'srv_diff_host_rate': 0.0,
                
                # Label
                'label': label
            }
            
            ids_data.append(packet)
            
            if (idx + 1) % 1000 == 0:
                print(f"   Processed {idx + 1} packets...")
                
        except Exception as e:
            print(f"   Warning: Error processing packet {idx}: {e}")
            continue
    
    # Create DataFrame
    df_ids = pd.DataFrame(ids_data)
    
    print(f"\n3. Saving to: {output_path}")
    df_ids.to_csv(output_path, index=False)
    print(f"   ✓ Saved {len(df_ids)} packets")
    
    print(f"\n4. Summary:")
    print(f"   Total packets: {len(df_ids)}")
    print(f"   Label: {label}")
    print(f"   Protocol distribution:")
    print(df_ids['protocol_type'].value_counts().to_string())
    print(f"\n   Service distribution:")
    print(df_ids['service'].value_counts().head(10).to_string())
    
    print(f"\n{'='*60}")
    print("✓ CONVERSION COMPLETED")
    print(f"{'='*60}\n")
    
    return df_ids


def merge_wireshark_datasets(normal_csv, attack_csv, output_path):
    """
    Merge normal and attack Wireshark datasets into training data
    
    Args:
        normal_csv: Path to normal traffic CSV
        attack_csv: Path to attack traffic CSV  
        output_path: Path to save merged training data
    """
    print(f"\n{'='*60}")
    print("MERGING WIRESHARK DATASETS")
    print(f"{'='*60}\n")
    
    # Read both datasets
    print("1. Reading datasets...")
    df_normal = pd.read_csv(normal_csv)
    df_attack = pd.read_csv(attack_csv)
    print(f"   ✓ Normal traffic: {len(df_normal)} samples")
    print(f"   ✓ Attack traffic: {len(df_attack)} samples")
    
    # Merge
    print("\n2. Merging datasets...")
    df_merged = pd.concat([df_normal, df_attack], ignore_index=True)
    
    # Shuffle
    print("3. Shuffling data...")
    df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    print(f"\n4. Saving to: {output_path}")
    df_merged.to_csv(output_path, index=False)
    
    print(f"\n5. Final dataset:")
    print(f"   Total samples: {len(df_merged)}")
    print(f"   Label distribution:")
    print(df_merged['label'].value_counts().to_string())
    
    print(f"\n{'='*60}")
    print("✓ MERGE COMPLETED")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Wireshark data to IDS format')
    
    parser.add_argument('--wireshark-csv', type=str,
                        help='Path to Wireshark CSV export')
    parser.add_argument('--output', type=str,
                        help='Output path for converted data')
    parser.add_argument('--label', type=str, default='normal',
                        choices=['normal', 'attack'],
                        help='Label for this data (normal or attack)')
    parser.add_argument('--merge-normal', type=str,
                        help='Path to normal traffic CSV for merging')
    parser.add_argument('--merge-attack', type=str,
                        help='Path to attack traffic CSV for merging')
    parser.add_argument('--merge-output', type=str,
                        help='Output path for merged training data')
    
    args = parser.parse_args()
    
    if args.merge_normal and args.merge_attack and args.merge_output:
        # Merge mode
        merge_wireshark_datasets(args.merge_normal, args.merge_attack, args.merge_output)
    elif args.wireshark_csv and args.output:
        # Convert mode
        convert_wireshark_to_ids(args.wireshark_csv, args.output, args.label)
    else:
        parser.print_help()

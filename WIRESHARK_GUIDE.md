# 📡 Menggunakan Data Wireshark dengan IDS System

## 🎯 Overview

Sistem IDS ini sekarang mendukung data dari **Wireshark packet capture**! Anda bisa:
1. Capture traffic real dengan Wireshark
2. Convert ke format IDS
3. Train model dengan data real
4. Detect attack dari traffic real

---

## 📋 **Langkah-langkah Menggunakan Data Wireshark:**

### **Step 1: Capture Traffic dengan Wireshark** 📡

#### **1.1 Install Wireshark**
```bash
# Download dari: https://www.wireshark.org/download.html
# Install dengan default settings
```

#### **1.2 Capture Normal Traffic**
```
1. Buka Wireshark
2. Pilih network interface (WiFi/Ethernet)
3. Klik "Start Capturing"
4. Lakukan aktivitas normal:
   - Browsing web
   - Download file
   - Streaming video
   - Email
5. Capture selama 5-10 menit
6. Stop capture
7. File → Export Packet Dissections → As CSV
8. Save as: normal_traffic.csv
```

**Kolom yang perlu di-export:**
- `frame.time_relative`
- `ip.proto`
- `ip.src`
- `ip.dst`
- `tcp.dstport` atau `udp.dstport`
- `tcp.flags`
- `frame.len`
- `ip.len`

#### **1.3 Capture Attack Traffic (Simulasi)**
```
Untuk simulasi attack, Anda bisa:

1. Port Scan:
   - Gunakan nmap: nmap -sS target_ip
   - Capture traffic saat scan

2. DoS Simulation (HANYA untuk testing lab):
   - Gunakan hping3 (Linux)
   - JANGAN lakukan ke sistem production!

3. Brute Force:
   - Simulasi failed login attempts
   - Capture traffic

4. Atau gunakan dataset public:
   - CICIDS2017
   - NSL-KDD
```

---

### **Step 2: Convert Wireshark CSV ke Format IDS** 🔄

```bash
cd "C:\CODING\CRYPTO FINAL"

# Convert normal traffic
python data/wireshark_converter.py \
    --wireshark-csv path/to/normal_traffic.csv \
    --output data/wireshark_normal.csv \
    --label normal

# Convert attack traffic
python data/wireshark_converter.py \
    --wireshark-csv path/to/attack_traffic.csv \
    --output data/wireshark_attack.csv \
    --label attack
```

**Output:**
```
============================================================
WIRESHARK TO IDS CONVERTER
============================================================

1. Reading Wireshark CSV: normal_traffic.csv
   ✓ Loaded 5000 packets
   ✓ Columns: 15

2. Converting to IDS format...
   Processed 1000 packets...
   Processed 2000 packets...
   ...

3. Saving to: data/wireshark_normal.csv
   ✓ Saved 5000 packets

4. Summary:
   Total packets: 5000
   Label: normal
   Protocol distribution:
   tcp     4500
   udp      450
   icmp      50

============================================================
✓ CONVERSION COMPLETED
============================================================
```

---

### **Step 3: Merge Normal + Attack Data** 🔗

```bash
# Merge kedua dataset menjadi training data
python data/wireshark_converter.py \
    --merge-normal data/wireshark_normal.csv \
    --merge-attack data/wireshark_attack.csv \
    --merge-output data/wireshark_training.csv
```

**Output:**
```
============================================================
MERGING WIRESHARK DATASETS
============================================================

1. Reading datasets...
   ✓ Normal traffic: 5000 samples
   ✓ Attack traffic: 2000 samples

2. Merging datasets...
3. Shuffling data...

4. Saving to: data/wireshark_training.csv

5. Final dataset:
   Total samples: 7000
   Label distribution:
   normal    5000
   attack    2000

============================================================
✓ MERGE COMPLETED
============================================================
```

---

### **Step 4: Train Model dengan Data Wireshark** 🤖

```bash
# Update config untuk use Wireshark data
# Edit config.py:
# TRAINING_DATA_PATH = 'data/wireshark_training.csv'

# Train model
python models/ml_model.py
```

**Output:**
```
============================================================
TRAINING IDS MACHINE LEARNING MODEL
============================================================

1. Loading training data from: data/wireshark_training.csv
   ✓ Loaded 7000 samples
   ✓ Features: 28

2. Label distribution:
   - normal: 5000 (71.4%)
   - attack: 2000 (28.6%)

...

6. Evaluating model performance...
   Accuracy: 96.50%  ← Bisa lebih rendah dari synthetic data

✓ MODEL TRAINING COMPLETED SUCCESSFULLY
============================================================
```

---

### **Step 5: Test dengan Data Real** 🧪

```bash
# Upload Wireshark CSV ke dashboard
1. Buka http://localhost:5000
2. Klik "Upload CSV"
3. Pilih: wireshark_training.csv
4. Lihat hasil deteksi!
```

---

## 🔍 **Feature Mapping: Wireshark → IDS**

### **Direct Mapping:**

| Wireshark Field | IDS Feature | Description |
|----------------|-------------|-------------|
| `frame.time_relative` | `duration` | Time since capture start |
| `ip.proto` | `protocol_type` | Protocol (tcp/udp/icmp) |
| `tcp.dstport` | `service` | Destination port → service |
| `tcp.flags` | `flag` | TCP flags → connection state |
| `frame.len` | `src_bytes` | Frame length |
| `ip.len` | `dst_bytes` | IP packet length |

### **Derived Features:**

| IDS Feature | How It's Calculated |
|------------|---------------------|
| `land` | Check if `ip.src == ip.dst` |
| `wrong_fragment` | Check for `tcp.analysis.retransmission` |
| `urgent` | Check `tcp.urgent_pointer > 0` |
| `count` | Count packets per connection |
| `serror_rate` | Calculate from TCP flags |

### **Features yang Perlu Analisis Lebih Dalam:**

Beberapa features butuh analisis application layer:
- `num_failed_logins` - Perlu inspect payload
- `logged_in` - Perlu inspect payload
- `hot` - Perlu inspect payload
- `num_compromised` - Perlu inspect payload

**Untuk prototype, features ini di-set default value.**

---

## 📊 **Contoh: Export Wireshark ke CSV**

### **Di Wireshark:**

```
1. File → Export Packet Dissections → As CSV

2. Pilih kolom yang di-export:
   ☑ frame.number
   ☑ frame.time_relative
   ☑ ip.src
   ☑ ip.dst
   ☑ ip.proto
   ☑ ip.len
   ☑ tcp.srcport
   ☑ tcp.dstport
   ☑ tcp.flags
   ☑ tcp.stream
   ☑ frame.len
   ☑ udp.srcport
   ☑ udp.dstport

3. Save as CSV
```

### **Contoh CSV Output:**

```csv
frame.number,frame.time_relative,ip.src,ip.dst,ip.proto,tcp.dstport,tcp.flags,frame.len
1,0.000000,192.168.1.100,142.250.185.46,6,443,0x00000002,74
2,0.001234,142.250.185.46,192.168.1.100,6,54321,0x00000012,74
3,0.002456,192.168.1.100,142.250.185.46,6,443,0x00000010,1514
```

---

## ⚠️ **Limitasi & Catatan:**

### **1. Feature Extraction Terbatas**

Wireshark packet capture hanya punya informasi network layer. Beberapa IDS features butuh:
- Application layer analysis
- Connection state tracking
- Historical data

**Solusi:** Converter menggunakan estimasi/default values untuk features yang tidak bisa di-extract.

### **2. Accuracy Bisa Lebih Rendah**

Model trained dengan synthetic data: **98%+ accuracy**
Model trained dengan Wireshark data: **90-96% accuracy**

**Alasan:**
- Real traffic lebih noisy
- Features tidak lengkap
- Variasi lebih besar

**Ini NORMAL dan acceptable!**

### **3. Butuh Label Manual**

Untuk training, Anda harus tahu mana traffic normal dan mana attack.

**Cara:**
- Capture normal traffic saat aktivitas normal
- Capture attack traffic saat simulasi attack
- Atau gunakan dataset labeled (CICIDS2017, NSL-KDD)

---

## 🎯 **Rekomendasi:**

### **Untuk Project Akademik:**

**Opsi 1: Hybrid Approach (Recommended)** ✅
```
1. Train dengan synthetic data (generator.py)
   - Akurasi tinggi
   - Mudah dikontrol
   - Cukup untuk demo

2. Test dengan Wireshark data (real traffic)
   - Tunjukkan sistem bisa handle real data
   - Lebih impressive
   - Proof of concept
```

**Opsi 2: Full Wireshark Data**
```
1. Capture traffic real (butuh waktu)
2. Label manual (normal vs attack)
3. Train model
4. Test

Lebih realistis tapi lebih kompleks.
```

### **Untuk Presentasi:**

```
"Sistem ini di-train dengan synthetic data yang mensimulasikan
network traffic patterns. Namun, sistem juga mendukung data real
dari Wireshark packet capture.

Kami menyediakan converter untuk transform Wireshark CSV ke format
IDS, sehingga sistem bisa di-deploy dengan real network traffic.

Untuk production deployment, model bisa di-retrain dengan data
capture real dari environment target."
```

---

## ✅ **Quick Start dengan Wireshark:**

```bash
# 1. Capture traffic dengan Wireshark
# 2. Export as CSV

# 3. Convert
python data/wireshark_converter.py \
    --wireshark-csv your_capture.csv \
    --output data/wireshark_data.csv \
    --label normal

# 4. Upload ke dashboard
# Buka http://localhost:5000
# Upload wireshark_data.csv

# Done!
```

---

## 📚 **Resources:**

- **Wireshark Download:** https://www.wireshark.org/download.html
- **Wireshark User Guide:** https://www.wireshark.org/docs/wsug_html_chunked/
- **CICIDS2017 Dataset:** https://www.unb.ca/cic/datasets/ids-2017.html
- **NSL-KDD Dataset:** https://www.unb.ca/cic/datasets/nsl.html

---

**Sekarang sistem Anda siap untuk data Wireshark!** 🎉

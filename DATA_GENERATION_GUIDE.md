# 📊 Cara Membuat Data Training CSV - Penjelasan Lengkap

## 🎯 Overview

Data training CSV dibuat menggunakan script `data/generator.py` yang menghasilkan **synthetic network traffic data** dengan pola normal dan attack yang realistis.

---

## 🔧 Cara Generate Data Training

### Metode 1: Command Line (Recommended)

```bash
cd "C:\CODING\CRYPTO FINAL"
python data/generator.py --generate-training --samples 10000
```

**Output:**
```
Generating 10000 training samples...
  Generated 1000 normal samples...
  Generated 2000 normal samples...
  ...
  Generated 7000 normal samples...
  Generated 1000 attack samples...
  ...
✓ Training data saved to data\training_data.csv
  Normal: 7000 samples
  Attack: 3000 samples
  Total: 10000 samples
```

### Metode 2: Python Script

```python
from data.generator import generate_training_data

# Generate 10,000 samples
df = generate_training_data(
    num_samples=10000,
    output_path='data/training_data.csv'
)
```

---

## 📋 Struktur Data yang Dihasilkan

### 28 Kolom Features + 1 Label

File CSV yang dihasilkan memiliki **29 kolom**:

#### 1. Basic Connection Features (5 kolom)
- `duration` - Durasi koneksi (detik)
- `protocol_type` - Protokol: tcp, udp, icmp
- `service` - Service: http, ftp, smtp, ssh, dns, telnet, private
- `flag` - Status flag: SF, S0, REJ, RSTR, SH, S1, S2, S3
- `src_bytes` - Bytes dikirim dari source
- `dst_bytes` - Bytes dikirim ke destination

#### 2. Content Features (13 kolom)
- `land` - 1 jika source = destination, 0 jika tidak
- `wrong_fragment` - Jumlah fragment yang salah
- `urgent` - Jumlah urgent packets
- `hot` - Jumlah "hot" indicators
- `num_failed_logins` - Jumlah login gagal
- `logged_in` - 1 jika berhasil login, 0 jika tidak
- `num_compromised` - Jumlah compromised conditions
- `root_shell` - 1 jika ada root shell, 0 jika tidak
- `su_attempted` - Jumlah percobaan "su root"
- `num_root` - Jumlah root accesses
- `num_file_creations` - Jumlah file operations
- `num_shells` - Jumlah shell prompts
- `num_access_files` - Jumlah akses ke access control files

#### 3. Traffic Features (10 kolom)
- `count` - Jumlah koneksi ke host yang sama
- `srv_count` - Jumlah koneksi ke service yang sama
- `serror_rate` - % koneksi dengan "SYN" errors
- `srv_serror_rate` - % koneksi dengan "SYN" errors (same service)
- `rerror_rate` - % koneksi dengan "REJ" errors
- `srv_rerror_rate` - % koneksi dengan "REJ" errors (same service)
- `same_srv_rate` - % koneksi ke service yang sama
- `diff_srv_rate` - % koneksi ke service berbeda
- `srv_diff_host_rate` - % koneksi ke host berbeda (same service)

#### 4. Label (1 kolom)
- `label` - 'normal' atau 'attack'

---

## 🎨 Bagaimana Data Dibuat?

### 1. Generate Normal Traffic

```python
def generate_normal_traffic():
    return {
        'duration': np.random.exponential(10),  # Durasi normal
        'protocol_type': random.choice(['tcp', 'udp']),  # Protokol umum
        'service': random.choice(['http', 'ftp', 'smtp', 'dns']),
        'flag': random.choice(['SF', 'S0']),  # Flag normal
        'src_bytes': np.random.randint(50, 5000),  # Bytes normal
        'dst_bytes': np.random.randint(50, 5000),
        'land': 0,  # Tidak ada land attack
        'num_failed_logins': 0,  # Tidak ada failed login
        'logged_in': 1,  # Berhasil login
        'count': np.random.randint(1, 100),  # Connection count normal
        'serror_rate': np.random.uniform(0, 0.1),  # Error rate rendah
        'same_srv_rate': np.random.uniform(0.8, 1.0),  # High same service
        # ... dst
        'label': 'normal'
    }
```

**Karakteristik Normal Traffic:**
- ✅ Durasi koneksi normal (exponential distribution)
- ✅ Protokol umum (tcp, udp)
- ✅ Service legitimate (http, ftp, smtp, dns)
- ✅ Berhasil login (logged_in = 1)
- ✅ Error rate rendah (< 10%)
- ✅ Connection count normal (1-100)

### 2. Generate Attack Traffic

Ada **4 tipe attack** yang disimulasikan:

#### A. DoS (Denial of Service)
```python
{
    'duration': 0,  # Koneksi sangat cepat
    'protocol_type': 'tcp',
    'service': random.choice(['http', 'private']),
    'flag': random.choice(['S0', 'REJ', 'RSTR']),  # Flag error
    'src_bytes': 0,  # Tidak ada data
    'dst_bytes': 0,
    'count': np.random.randint(200, 500),  # BANYAK koneksi
    'serror_rate': np.random.uniform(0.9, 1.0),  # Error rate TINGGI
    'same_srv_rate': np.random.uniform(0.9, 1.0),  # Semua ke service sama
    'label': 'attack'
}
```

**Karakteristik DoS:**
- 🚨 Durasi = 0 (koneksi instant)
- 🚨 Bytes = 0 (tidak ada data transfer)
- 🚨 Count tinggi (200-500 koneksi)
- 🚨 Error rate sangat tinggi (90-100%)

#### B. Port Scan
```python
{
    'duration': 0,
    'protocol_type': random.choice(['tcp', 'icmp']),
    'service': 'private',
    'count': np.random.randint(100, 300),  # Banyak koneksi
    'srv_count': np.random.randint(1, 10),  # Sedikit service
    'diff_srv_rate': np.random.uniform(0.8, 1.0),  # BANYAK service berbeda
    'serror_rate': np.random.uniform(0.5, 1.0),  # Error tinggi
    'label': 'attack'
}
```

**Karakteristik Port Scan:**
- 🚨 Koneksi ke banyak port berbeda
- 🚨 diff_srv_rate tinggi (80-100%)
- 🚨 Error rate tinggi

#### C. DDoS (Distributed DoS)
```python
{
    'count': np.random.randint(300, 600),  # SANGAT banyak koneksi
    'srv_count': np.random.randint(300, 600),
    'serror_rate': np.random.uniform(0.8, 1.0),  # Error sangat tinggi
    'srv_diff_host_rate': np.random.uniform(0.8, 1.0),  # Dari banyak host
    'label': 'attack'
}
```

**Karakteristik DDoS:**
- 🚨 Count SANGAT tinggi (300-600)
- 🚨 Dari banyak host berbeda
- 🚨 Error rate sangat tinggi

#### D. Brute Force
```python
{
    'service': random.choice(['ftp', 'ssh', 'telnet']),  # Login services
    'num_failed_logins': np.random.randint(1, 10),  # BANYAK failed login
    'logged_in': 0,  # Gagal login
    'rerror_rate': np.random.uniform(0.3, 0.8),  # Rejection tinggi
    'label': 'attack'
}
```

**Karakteristik Brute Force:**
- 🚨 Banyak failed login attempts
- 🚨 Service: ftp, ssh, telnet
- 🚨 Rejection rate tinggi

---

## 📊 Distribusi Data

### Default: 70% Normal, 30% Attack

```python
num_normal = int(num_samples * 0.7)  # 70% normal
num_attack = num_samples - num_normal  # 30% attack
```

**Untuk 10,000 samples:**
- ✅ 7,000 normal traffic
- 🚨 3,000 attack traffic (campuran DoS, Port Scan, DDoS, Brute Force)

### Data Di-Shuffle

```python
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle random
```

Data di-shuffle agar tidak berurutan (normal semua dulu, baru attack).

---

## 🎯 Contoh Data yang Dihasilkan

### Sample Normal Traffic
```csv
duration,protocol_type,service,flag,src_bytes,dst_bytes,land,wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,root_shell,su_attempted,num_root,num_file_creations,num_shells,num_access_files,count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate,label
8.5,tcp,http,SF,1234,2345,0,0,0,1,0,1,0,0,0,0,2,0,1,45,50,0.05,0.03,0.02,0.01,0.95,0.05,0.10,normal
```

### Sample Attack Traffic (DoS)
```csv
0,tcp,http,S0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,350,340,0.98,0.97,0,0,0.99,0.01,0,attack
```

---

## 🚀 Cara Menggunakan Data

### 1. Generate Data Baru
```bash
# Generate 10,000 samples
python data/generator.py --generate-training --samples 10000

# Generate 50,000 samples (lebih banyak)
python data/generator.py --generate-training --samples 50000
```

### 2. Lihat Data
```bash
# Buka dengan Excel/LibreOffice
# Atau dengan pandas:
python -c "import pandas as pd; df = pd.read_csv('data/training_data.csv'); print(df.head())"
```

### 3. Train Model
```bash
python models/ml_model.py
```

### 4. Upload ke Dashboard
- Buka dashboard: http://localhost:5000
- Klik "Upload CSV"
- Pilih: `data/training_data.csv` atau `data/sample_upload.csv`

---

## 💡 Tips & Customization

### Ubah Rasio Normal vs Attack
Edit `generator.py` line 205-206:
```python
num_normal = int(num_samples * 0.8)  # 80% normal (lebih aman)
num_attack = num_samples - num_normal  # 20% attack
```

### Tambah Tipe Attack Baru
Tambahkan di fungsi `generate_attack_traffic()`:
```python
elif attack_type == 'SQL Injection':
    return {
        'service': 'http',
        'src_bytes': np.random.randint(100, 1000),
        # ... karakteristik SQL injection
        'label': 'attack'
    }
```

### Generate Data Lebih Cepat
Untuk dataset besar, gunakan multiprocessing (advanced).

---

## 📁 File Output

Setelah generate, file akan tersimpan di:
```
C:\CODING\CRYPTO FINAL\data\training_data.csv
```

**Size:** ~1-2 MB untuk 10,000 samples

**Format:** CSV dengan header, compatible dengan pandas, Excel, dan ML libraries.

---

## ✅ Kesimpulan

Data training CSV dibuat dengan:
1. **Fungsi generate_normal_traffic()** - Buat traffic normal
2. **Fungsi generate_attack_traffic()** - Buat 4 tipe attack
3. **Distribusi 70:30** - 70% normal, 30% attack
4. **Random shuffle** - Data tidak berurutan
5. **Save to CSV** - Format standard CSV

Data ini kemudian digunakan untuk:
- ✅ Train Random Forest model
- ✅ Test model accuracy
- ✅ Upload ke dashboard untuk analisis

---

<div align="center">

**🎯 Sekarang Anda Tahu Cara Data Training Dibuat!**

Silakan generate data baru atau modify generator sesuai kebutuhan!

</div>

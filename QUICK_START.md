# 🚀 Quick Start Guide - IDS ML Dashboard

## ✅ Status: Aplikasi Siap Digunakan!

Aplikasi IDS Machine Learning Dashboard sudah berhasil dibuat dan server Flask sedang berjalan!

---

## 📍 Akses Dashboard

**URL:** `http://localhost:5000`

Buka browser Anda (Chrome, Firefox, Edge) dan akses URL di atas.

---

## 🎮 Cara Menggunakan Dashboard

### 1️⃣ Start Monitoring
- Klik tombol **"Start Monitoring"** (hijau) di Control Panel
- Sistem akan mulai memantau traffic secara real-time
- Status indicator akan berubah sesuai kondisi (SAFE/WARNING/DANGER)

### 2️⃣ Simulasi Traffic Real-time
Buka **terminal baru** dan jalankan:
```bash
cd "C:\CODING\CRYPTO FINAL"
python data/generator.py --simulate-stream --interval 3
```

Ini akan mensimulasikan traffic baru setiap 3 detik.

### 3️⃣ Upload CSV untuk Analisis Batch
- Klik tombol **"Upload CSV"**
- Pilih file CSV dengan format yang sama seperti `training_data.csv`
- Sistem akan menganalisis semua data sekaligus

### 4️⃣ Stop Monitoring
- Klik tombol **"Stop Monitoring"** (merah) untuk menghentikan monitoring

---

## 📊 Fitur Dashboard

### Status Indicator
- 🟢 **SAFE** - Kurang dari 10% serangan
- 🟡 **WARNING** - 10-30% serangan  
- 🔴 **DANGER** - Lebih dari 30% serangan

### Statistics Cards
- **Total Packets** - Jumlah total paket yang dianalisis
- **Detected Attacks** - Jumlah serangan yang terdeteksi
- **Detection Rate** - Persentase serangan

### Traffic Distribution Chart
- Grafik donut menampilkan distribusi Normal vs Attack traffic
- Update otomatis setiap 2 detik

### Detection Logs Table
- Tabel log deteksi terbaru (20 entries)
- Menampilkan timestamp, prediction, confidence, threat type
- Auto-refresh tanpa reload halaman

### Last Detected Threat Panel
- Detail serangan terakhir yang terdeteksi
- Informasi: waktu, tipe threat, confidence, protocol, service

---

## 🔧 Troubleshooting

### Server Tidak Jalan?
```bash
cd "C:\CODING\CRYPTO FINAL"
python app.py
```

### Port Sudah Digunakan?
Edit `config.py`, ubah:
```python
PORT = 5001  # atau port lain yang tersedia
```

### Model Belum Di-train?
```bash
python data/generator.py --generate-training --samples 10000
python models/ml_model.py
```

---

## 📝 File Penting

| File | Fungsi |
|------|--------|
| `app.py` | Main Flask application |
| `data/training_data.csv` | Dataset training (10,000 samples) |
| `models/trained_model.pkl` | Model Random Forest yang sudah di-train |
| `database/ids_logs.db` | Database SQLite untuk logs |
| `README.md` | Dokumentasi lengkap |

---

## 🎯 Tips Penggunaan

1. **Untuk Demo**: 
   - Start monitoring
   - Jalankan stream simulator
   - Tunggu beberapa detik untuk melihat update real-time

2. **Untuk Testing**:
   - Upload file CSV batch
   - Lihat hasil analisis di logs table

3. **Untuk Presentasi**:
   - Tunjukkan status indicator yang berubah warna
   - Highlight chart yang update otomatis
   - Demo control panel (start/stop)

---

## 🛡️ Teknologi yang Digunakan

- **Backend**: Python Flask
- **ML**: scikit-learn (Random Forest)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Theme**: Cybersecurity Dark Mode

---

## 📞 Support

Jika ada masalah, cek:
1. `README.md` - Dokumentasi lengkap
2. `walkthrough.md` - Penjelasan detail project
3. Terminal output - Error messages

---

<div align="center">

**✅ Aplikasi Siap Digunakan!**

Buka browser dan akses: **http://localhost:5000**

🛡️ **Stay Safe, Stay Secure** 🛡️

</div>

# 🔧 Troubleshooting Guide - IDS ML Dashboard

## ❌ Error: Upload CSV Gagal

### Masalah
Error saat upload CSV: `"None of [Index(...)] are in the [columns]"`

### Penyebab
File CSV yang di-upload tidak memiliki kolom yang sesuai dengan format training data.

### ✅ Solusi

**1. Gunakan File Template yang Benar**

File CSV harus memiliki kolom yang sama dengan `training_data.csv`. Gunakan salah satu file berikut sebagai template:

- `data/training_data.csv` - Dataset lengkap (10,000 rows)
- `data/sample_upload.csv` - Sample kecil (50 rows) untuk testing

**2. Format CSV yang Benar**

File CSV harus memiliki kolom-kolom berikut:

```
duration,protocol_type,service,flag,src_bytes,dst_bytes,land,wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,root_shell,su_attempted,num_root,num_file_creations,num_shells,num_access_files,count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate,label
```

**3. Cara Upload yang Benar**

```bash
# Di dashboard:
1. Klik tombol "Upload CSV"
2. Pilih file: data/sample_upload.csv atau data/training_data.csv
3. Tunggu proses selesai
4. Lihat hasil di statistics dan logs table
```

**4. Generate Sample CSV untuk Testing**

Jika ingin membuat sample CSV sendiri:

```bash
cd "C:\CODING\CRYPTO FINAL"
python -c "import pandas as pd; df = pd.read_csv('data/training_data.csv'); df.head(50).to_csv('data/sample_upload.csv', index=False)"
```

---

## ❌ Error: Favicon 404

### Masalah
`Failed to load resource: favicon.ico 404 NOT FOUND`

### Penyebab
Browser mencari favicon yang tidak ada.

### ✅ Solusi
Error ini tidak mempengaruhi fungsi aplikasi. Bisa diabaikan atau tambahkan favicon di folder `static/`.

---

## ❌ Error: Server Tidak Bisa Diakses

### Masalah
Dashboard tidak bisa dibuka di browser

### ✅ Solusi

**1. Pastikan Server Berjalan**
```bash
# Cek terminal, harus ada output:
# * Running on http://0.0.0.0:5000
```

**2. Restart Server**
```bash
# Tekan Ctrl+C di terminal
# Kemudian jalankan lagi:
python app.py
```

**3. Cek Port**
Pastikan port 5000 tidak digunakan aplikasi lain.

---

## ❌ Error: Model Not Found

### Masalah
`ML model not found. Please train the model first.`

### ✅ Solusi
```bash
# Generate training data
python data/generator.py --generate-training --samples 10000

# Train model
python models/ml_model.py
```

---

## ❌ Error: Monitoring Tidak Jalan

### Masalah
Setelah klik "Start Monitoring", tidak ada data yang masuk

### ✅ Solusi

**1. Pastikan Stream File Ada**
```bash
# Jalankan stream simulator di terminal baru:
python data/generator.py --simulate-stream --interval 3
```

**2. Cek Status Monitoring**
- Di dashboard, lihat "Monitoring: Active" di control panel
- Jika "Stopped", klik "Start Monitoring" lagi

---

## ✅ Cara Testing yang Benar

### Test 1: Upload CSV
```bash
1. Buka dashboard: http://localhost:5000
2. Klik "Upload CSV"
3. Pilih: data/sample_upload.csv
4. Tunggu notifikasi success
5. Lihat statistics bertambah
```

### Test 2: Real-time Monitoring
```bash
# Terminal 1: Server
python app.py

# Terminal 2: Stream Simulator
python data/generator.py --simulate-stream --interval 3

# Browser:
1. Buka http://localhost:5000
2. Klik "Start Monitoring"
3. Lihat status, chart, dan logs update otomatis
```

---

## 📋 Checklist Sebelum Upload CSV

- [ ] File berformat `.csv`
- [ ] File memiliki header (baris pertama adalah nama kolom)
- [ ] File memiliki semua 28 kolom yang required
- [ ] Kolom `label` boleh ada atau tidak (akan dihapus otomatis)
- [ ] Data dalam kolom sesuai tipe (angka untuk numerical, text untuk categorical)

---

## 🔍 Debug Tips

### Lihat Error Detail di Terminal
Saat upload gagal, cek terminal server untuk error detail:
```
Upload error: [detail error]
```

### Test API Langsung
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test status endpoint
curl http://localhost:5000/api/status
```

### Cek Database
```bash
# Lihat isi database
python -c "from database.models import get_database; db = get_database('database/ids_logs.db'); print(db.get_statistics())"
```

---

## 📞 Bantuan Lebih Lanjut

Jika masih ada masalah:

1. **Cek README.md** - Dokumentasi lengkap
2. **Cek terminal output** - Error messages
3. **Restart aplikasi** - Kadang solve banyak masalah
4. **Regenerate data** - Hapus dan buat ulang training data

---

<div align="center">

**✅ Server sudah di-restart dengan fix upload CSV!**

Silakan coba upload lagi dengan file: `data/sample_upload.csv`

</div>

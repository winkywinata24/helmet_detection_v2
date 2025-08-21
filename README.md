# Helmet Detection v2 🚴‍♂️🪖

Proyek Akhir ini bertujuan untuk membangun sistem **deteksi helm** beserta **chin strap** menggunakan algoritma **YOLO**.  
Sistem terdiri dari tiga bagian utama:  

1. **Android**  
   - Aplikasi mobile untuk menampilkan streaming video dari CCTV.  
   - Menampilkan hasil deteksi (notifikasi pelanggaran) secara real-time.  
   - Berkomunikasi dengan server menggunakan **WebSocket** dan database.  

2. **Backend**  
   - Terdiri dari dua bagian:  
     - **Python (YOLO)**: menjalankan model deteksi helm dari CCTV (RTSP streaming).  
     - **PHP + MySQL**: API untuk menyimpan dan menampilkan hasil deteksi (log history).  

3. **Training**  
   - Berisi proses training model YOLO untuk mendeteksi helm.  
   - Dataset telah melalui proses preprocessing (augmentasi, normalisasi, splitting) yang dilakukan di **[Roboflow](https://app.roboflow.com/winky-ncblh/helmet-detection-uurgi)**.  
   - Folder training berisi konfigurasi, notebook eksperimen, dan hasil training.  

---

## 📂 Struktur Direktori

```
helmet_detection_v2/
├── Android/        # Proyek aplikasi Android
├── Backend/        # Server-side (YOLO + PHP API + database)
└── Training/       # Training YOLO (notebooks, models, results)
```

---

## ⚙️ Teknologi yang Digunakan

- **Deep Learning Model**: YOLO  
- **Server (Deteksi)**: Python  
- **API & Database**: PHP + MySQL (Laragon untuk development)  
- **Mobile App**: Android (Kotlin)  

---

## 🚀 Cara Menjalankan

### 1. Backend
1. Jalankan server Python untuk deteksi YOLO.  
2. Pastikan MySQL & Apache (Laragon/XAMPP) sudah berjalan.  
3. Letakkan file PHP API di folder  `www/helmet-api` (bawaan Laragon).  
4. Pastikan konfigurasi `db_config.php` sesuai dengan database MySQL.  

### 2. Android
1. Buka folder `Android/` di Android Studio.  
2. Ganti IP pada konfigurasi **WebSocket** dan **API URL** agar sesuai dengan server.  
3. Jalankan aplikasi di emulator atau device.  

### 3. Training
1. Masuk ke folder `Training/notebooks/`.  
2. Buka notebook `.ipynb` di JupyterLab / Colab.  
3. Jalankan cell sesuai urutan untuk training model.  

---

## 📊 Hasil dan Analisis
- Model YOLO berhasil mendeteksi **With Helmet, Without Helmet, With Chin Strap, Without Chin Strap**.  
- Pengujian dilakukan pada kondisi **terang** dan **gelap**.  
- Sistem memberikan notifikasi real-time ke aplikasi Android.  
- Kondisi **pencahayaan** dan **jarak objek dengan CCTV** sangat berpengaruh terhadap tingkat akurasi deteksi.  

---

## ✨ Kontributor
- **Winky Augeryan Winata** (Informatics Engineering Student – PCR)  
- **Ananda, S.Kom., M.T., Ph.D.** (Dosen Pembimbing Proyek Akhir – PCR)  

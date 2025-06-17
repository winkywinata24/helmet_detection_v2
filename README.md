# Helmet Detection System

Sistem ini mendeteksi pelanggaran penggunaan helm menggunakan kamera IP, model YOLO, dan mengirimkan notifikasi ke aplikasi Android secara real-time.

---

## 🧰 Peralatan yang Dibutuhkan

1. **Server** (PC/Laptop)
2. **HP Android**
3. **Router**
4. **IP Camera**

---

## 🔌 Setup Peralatan

1. Sambungkan **router** ke internet (jika diperlukan).
2. Sambungkan **server**, **IP Camera**, dan **HP Android** ke jaringan router yang sama (WiFi atau LAN).

---

## ⚙️ Setup Awal

### 🐍 Backend (Python)

1. Ganti RTSP URL di `main.py` (baris 21):
   ```python
   RTSP_URL = "rtsp://<username>:<password>@<ip_camera_ip>/stream1"
3. Ganti path model YOLO di `yolo_detection.py` (baris 6), jika menggunakan model lain:
   ```python
   model = torch.hub.load("ultralytics/yolov5", "custom", path="best.pt")
5. Buat database MySQL dengan nama `helmet_detection` (bisa menggunakan Laragon).
6. Buat tabel `log_history` dengan perintah SQL berikut:
   ```sql
   CREATE TABLE log_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        waktu DATETIME NOT NULL,
        status_helm TINYINT(1) NOT NULL,
        status_strap TINYINT(1) NOT NULL
   );
8. Pindahkan folder `helmet-api` ke folder www milik Laragon:
   ```makefile
   C:\laragon\www\helmet-api
   
### 📱 Aplikasi Android

1. Ganti RTSP URL di `HomeFragment.kt` (baris 51):
   ```kotlin
   val rtspUrl = "rtsp://<username>:<password>@<ip_camera_ip>/stream1"
3. Ganti BASE_URL API di `RetrofitClient.kt` (baris 7):
   ```kotlin
   const val BASE_URL = "http://<ip_server>/helmet-api/"

---
   
## 🚀 Menjalankan Sistem
### Server:
1. Jalankan `Apache` dan `MySQL` via Laragon.
2. Jalankan script Python:
   ```bash
   python main.py
   
### Android:
1. Jalankan aplikasi **Helmet Detection v2**.
2. Aplikasi akan menampilkan RTSP stream dan menerima notifikasi pelanggaran.

---

## ✅ Catatan Tambahan
1. Aplikasi tetap menerima notifikasi meskipun ditutup atau dihapus dari recent apps.
2. Notifikasi dikirim via WebSocket dan ditangani oleh foreground service.
3. Jika ingin mematikan deteksi, tambahkan fitur untuk menghentikan service.
4. Untuk mematikan audio dari kamera, atur volume ke nol:
   player?.volume = 0f

---
   
## 🌐 Arsitektur Jaringan
```css
[IP Camera] ─┐
             │
         [Router] ─── [Server (main.py)]
             │
       [Android Phone]

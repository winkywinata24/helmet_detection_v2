import cv2
import time
import asyncio
import threading
from yolo_detection import detect_helmet
from db_connection import insert_detection_result
from ws_server import start_server_main, send_notification, set_loop

# Jalankan server WebSocket di thread terpisah
def run_ws():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    set_loop(loop)
    loop.run_until_complete(start_server_main())
    loop.run_forever()
    

threading.Thread(target=run_ws, daemon=True).start()

# RTSP URL dari IP Camera
RTSP_URL = "rtsp://admin123:admin123@192.168.0.10/stream1"

# Daftar kelas pelanggaran
VIOLATION_CLASSES = ["Without Helmet", "Without Chin Strap"]

last_detected = {}
COOLDOWN_SECONDS = 5

def main():
    # Buka koneksi ke kamera RTSP
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        print("Gagal membuka stream RTSP.")
        return

    print("RTSP stream berhasil dibuka. Memulai deteksi...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membaca frame dari kamera.")
                time.sleep(1)
                continue

            # Kirim frame ke YOLO untuk deteksi
            detection_results = detect_helmet(frame)

            if detection_results is None:
                print("Tidak ada deteksi pada frame ini.")
                continue  # Tidak ada pelanggaran, lanjut loop

            # Simpan semua hasil deteksi ke database
            for result in detection_results:
                class_name = result["class_name"]
                timestamp = time.time()
                
                # Cek apakah class ini pernah terdeteksi sebelumnya
                if class_name in last_detected:
                    if timestamp - last_detected[class_name] < COOLDOWN_SECONDS:
                        continue  # Skip deteksi yang terlalu dekat waktunya
                    
                # Update waktu deteksi terakhir
                last_detected[class_name] = timestamp
                print("Detection results:", detection_results)
                insert_detection_result(result)
                
                # Kirim notifikasi hanya jika terdeteksi pelanggaran
                if class_name in VIOLATION_CLASSES:
                    print("Mengirim Notifikasi: ", result)
                    send_notification(result)
                else:
                    print("Tidak ada pelanggaran terdeteksi:", class_name)

    except KeyboardInterrupt:
        print("\nDeteksi dihentikan secara manual.")

    finally:
        cap.release()
        print("Koneksi kamera ditutup.")

if __name__ == "__main__":
    main()

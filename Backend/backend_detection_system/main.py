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
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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
            detection_results, annotated_frame = detect_helmet(frame)
            
            # Tampilkan preview kamera dengan hasil deteksi
            cv2.imshow("Preview Kamera - Deteksi Helm", annotated_frame)
            
            # Jika tombol 'q' ditekan, keluar dari loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if not detection_results:
                continue  # Tidak ada deteksi, lanjut loop

            # Status Default
            status_helm = 1
            status_strap = 1

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
                
                with open("detection_log.txt", "a") as log_file:
                    log_file.write(f"{detection_results}\n")

                if class_name == "With Helmet":
                    status_helm = 1
                elif class_name == "With Chin Strap":
                    status_strap = 1
                    status_helm = 1  # kalau ada strap, helm pasti ada
                elif class_name == "Without Helmet":
                    status_helm = 0
                    status_strap = 0 # kalau tidak ada helm, strap pasti tidak ada
                elif class_name == "Without Chin Strap":
                    status_strap = 0

                # Simpan sekali ke DB
                timestamp = detection_results[0]["timestamp"]
                insert_detection_result({
                    "timestamp": timestamp,
                    "status_helm": status_helm,
                    "status_strap": status_strap
                })

                # Kirim notifikasi
                type = "violation" if class_name in VIOLATION_CLASSES else "update"
                print("Mengirim Notifikasi: ", result)
                send_notification(result, type)
            
    except KeyboardInterrupt:
        print("\nDeteksi dihentikan secara manual.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Koneksi kamera ditutup.")

if __name__ == "__main__":
    main()

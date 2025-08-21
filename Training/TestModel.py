from ultralytics import YOLO
import cv2

# 1. Load model
model_path = "results/Hasil_Training_YOLOv11_3/train2/weights/best.pt"
model = YOLO(model_path)

# 2. Sumber video
source = 0  # webcam
cap = cv2.VideoCapture(source)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ambil ukuran frame
    h, w = frame.shape[:2]

    # Hitung crop untuk zoom 20% (10% kiri, 10% kanan, 10% atas, 10% bawah)
    crop_x = int(w * 0.1)
    crop_y = int(h * 0.1)
    cropped_frame = frame[crop_y:h - crop_y, crop_x:w - crop_x]

    # Resize ke ukuran asli agar tetap sama
    resized_frame = cv2.resize(cropped_frame, (w, h))

    # Prediksi YOLO pada frame yang sudah di-zoom
    results = model.predict(resized_frame, conf=0.5, verbose=False)

    # Gambar hasil deteksi
    annotated_frame = results[0].plot()

    # Tampilkan frame
    cv2.imshow("Real-Time Detection (Zoomed)", annotated_frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

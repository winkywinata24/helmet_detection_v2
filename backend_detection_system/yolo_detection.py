import cv2
from ultralytics import YOLO
from datetime import datetime

# Load model hasil training
model = YOLO("E:\\helmet_detection_project\\backend_detection_system\\weights.pt")

# Mapping index ke nama kelas
CLASS_NAMES = ["With Chin Strap", "With Helmet", "Without Chin Strap", "Without Helmet"]

def detect_helmet(frame):
    # Ubah frame BGR ke RGB karena YOLO pakai RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Ubah ukuran frame ke 416x416 dengan padding
    letterboxed = letterbox(rgb_frame, (416, 416), (0, 0, 0))

    # Lakukan prediksi
    results = model.predict(source=letterboxed, conf=0.5, verbose=False)

    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = CLASS_NAMES[cls_id]
            confidence = float(box.conf[0])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            detection_data = {
                "class_name": class_name,
                "confidence": confidence,
                "timestamp": timestamp
            }

            detections.append(detection_data)

    # Kalau tidak ada deteksi, return None
    if not detections:
        return None

    return detections

def letterbox(image, target_size, color):
    import numpy as np
    import cv2

    h, w = image.shape[:2]
    new_w, new_h = target_size

    scale = min(new_w / w, new_h / h)
    resized_w = int(w * scale)
    resized_h = int(h * scale)

    resized_image = cv2.resize(image, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

    # Buat kanvas hitam 416x416
    canvas = np.full((new_h, new_w, 3), color, dtype=np.uint8)

    # Hitung posisi padding
    top = (new_h - resized_h) // 2
    left = (new_w - resized_w) // 2

    # Tempelkan resized image ke tengah kanvas
    canvas[top:top+resized_h, left:left+resized_w] = resized_image

    return canvas

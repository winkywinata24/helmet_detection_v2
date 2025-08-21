from ultralytics import YOLO
from datetime import datetime

# Load model hasil training
model = YOLO("E:\\helmet_detection_project\\backend_detection_system\\best.pt")

# Mapping index ke nama kelas
CLASS_NAMES = ["With Chin Strap", "With Helmet", "Without Chin Strap", "Without Helmet"]

def detect_helmet(frame):
    # Kirim frame ke YOLO untuk deteksi
    results = model.predict(source=frame, conf=0.5, verbose=False)

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

    # Ambil frame hasil anotasi YOLO
    annotated_frame = results[0].plot()

    # Return hasil deteksi (atau None jika tidak ada) dan annotated frame
    return (detections if detections else None), annotated_frame

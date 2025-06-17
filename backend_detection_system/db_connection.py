import mysql.connector

# Konfigurasi database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "helmet_detection"
}

def insert_detection_result(detection):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        class_name = detection["class_name"]
        waktu = detection["timestamp"]

        # Konversi class_name menjadi boolean flags
        strapDetected = class_name == "With Chin Strap"
        helmDetected = class_name == "With Helmet"
        noStrapDetected = class_name == "Without Chin Strap"
        noHelmDetected = class_name == "Without Helmet"

        if strapDetected:
            status_helm = 1  # jika strap terdeteksi, helm pasti juga
        elif helmDetected:
            status_helm = 1
        elif noHelmDetected:
            status_helm = 0
        else:
            status_helm = 0

        if strapDetected:
            status_strap = 1
        elif noStrapDetected:
            status_strap = 0
        elif noHelmDetected:
            status_strap = 0  # tidak ada helm, otomatis tidak ada strap
        else:
            status_strap = 1

        query = """
            INSERT INTO log_history (waktu, status_helm, status_strap)
            VALUES (%s, %s, %s)
        """
        values = (waktu, status_helm, status_strap)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Gagal menyimpan ke database:", err)

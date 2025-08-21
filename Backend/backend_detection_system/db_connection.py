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

        waktu = detection["timestamp"]
        status_helm = detection["status_helm"]
        status_strap = detection["status_strap"]

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

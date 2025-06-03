import os
import requests
import time
import random
from datetime import datetime
import socket

DEVICE_ID = os.getenv("DEVICE_ID", socket.gethostname())
EDGE_SERVER_URL = os.getenv("EDGE_SERVER_URL", "http://localhost:8000/ingest")
INTERVAL_SECONDS = 5

def generate_sensor_data():
    return {
        "device_id": DEVICE_ID,
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def send_data():
    while True:
        payload = generate_sensor_data()
        try:
            response = requests.post(EDGE_SERVER_URL, json=payload)
            print(f"[{datetime.utcnow().isoformat()}] Sent from {DEVICE_ID} | Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    send_data()


from fastapi import FastAPI, Request
from influxdb import InfluxDBClient
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

# Connect to InfluxDB (adjust for your setup)
INFLUXDB_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.getenv("INFLUXDB_PORT", 8086))
INFLUXDB_DB = os.getenv("INFLUXDB_DB", "iot_edge")

client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
client.create_database(INFLUXDB_DB)
client.switch_database(INFLUXDB_DB)

# Data model
class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    timestamp: str

@app.post("/ingest")
async def ingest_data(data: SensorData):
    print(f"Received data: {data.dict()}")

    json_body = [
        {
            "measurement": "environment",
            "tags": {
                "device_id": data.device_id
            },
            "time": data.timestamp,
            "fields": {
                "temperature": data.temperature,
                "humidity": data.humidity
            }
        }
    ]

    client.write_points(json_body)
    return {"status": "success"}


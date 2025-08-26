# Solution Guide: GCP Pub/Sub Case Study 1 (IoT Device Data Ingestion)

## Prerequisites
- You are logged into the Google Cloud Console (https://console.cloud.google.com/).
- You have the project ID and required permissions for Pub/Sub and schema management.

---


### 1. Create a Pub/Sub Schema
1. In the Cloud Console, go to **Pub/Sub > Schemas**.
2. Click **Create schema**.
3. Choose **AVRO** or **Protocol Buffer**.
4. Define the schema with the following fields and types:
	 - `device_id`: string (required)
	 - `timestamp`: string or int (required, e.g., ISO8601 or epoch)
	 - `temperature`: float (required)
	 - `humidity`: float (required)

**Example AVRO schema:**
```json
{
	"type": "record",
	"name": "IoTSensorData",
	"fields": [
		{"name": "device_id", "type": "string"},
		{"name": "timestamp", "type": "string"},
		{"name": "temperature", "type": "float"},
		{"name": "humidity", "type": "float"}
	]
}
```

**Example valid message:**
```json
{
	"device_id": "sensor-001",
	"timestamp": "2025-08-26T12:00:00Z",
	"temperature": 23.5,
	"humidity": 60.2
}
```

5. Name the schema (e.g., `iot_sensor_schema`).
6. Click **Create**.

---

### 2. Create a Topic and Associate the Schema
1. Go to **Pub/Sub > Topics**.
2. Click **Create topic**.
3. Enter a topic name (e.g., `iot-sensor-topic-<student_id>`).
4. Under **Schema settings**, select the schema you created.
5. Set schema enforcement to **Enforce**.
6. Click **Create**.

---

### 3. Publish 3 Valid Messages
1. Click your topic, then **Publish message**.
2. Enter valid JSON or binary data matching the schema (e.g., all required fields present and correct types).
3. Publish at least 3 messages.
4. Log each successful publish in your `test_report.log`.

---

### 4. Attempt to Publish an Invalid Message
1. Try publishing a message missing a required field or with a wrong type.
2. Confirm the message is rejected (error shown in console).
3. Log the error/result in your `test_report.log`.

---

### 5. Create a Subscription and Pull Messages
1. In your topic, click **Create subscription**.
2. Name the subscription (e.g., `iot-sensor-sub-<student_id>`).
3. Use default settings and create.
4. Click the subscription, then **Pull** to view received messages.
5. Log the received messages in your `test_report.log`.

---

**Tip:** Log every action and result for evaluation. If you get stuck, use the Cloud Console help or ask your instructor.

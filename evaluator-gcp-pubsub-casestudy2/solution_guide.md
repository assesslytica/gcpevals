# Solution Guide: GCP Pub/Sub Case Study 2 (Financial Transaction Processing)

## Prerequisites
- You are logged into the Google Cloud Console (https://console.cloud.google.com/).
- You have the project ID and required permissions for Pub/Sub and schema management.

---


### 1. Define a Pub/Sub Schema
1. Go to **Pub/Sub > Schemas** in the Cloud Console.
2. Click **Create schema**.
3. Choose **AVRO** or **Protocol Buffer**.
4. Define the schema with the following fields and types:
	 - `transaction_id`: string (required)
	 - `user_id`: string (required)
	 - `amount`: float (required)
	 - `currency`: string (required, e.g., "USD")
	 - `timestamp`: string or int (required, e.g., ISO8601 or epoch)

**Example AVRO schema:**
```json
{
	"type": "record",
	"name": "TransactionData",
	"fields": [
		{"name": "transaction_id", "type": "string"},
		{"name": "user_id", "type": "string"},
		{"name": "amount", "type": "float"},
		{"name": "currency", "type": "string"},
		{"name": "timestamp", "type": "string"}
	]
}
```

**Example valid message:**
```json
{
	"transaction_id": "txn-1001",
	"user_id": "user-42",
	"amount": 150.75,
	"currency": "USD",
	"timestamp": "2025-08-26T12:00:00Z"
}
```

5. Name the schema (e.g., `transaction_schema`).
6. Click **Create**.

---

### 2. Create a Topic and Enforce the Schema
1. Go to **Pub/Sub > Topics**.
2. Click **Create topic**.
3. Enter a topic name (e.g., `transaction-topic-<student_id>`).
4. Under **Schema settings**, select the schema you created.
5. Set schema enforcement to **Enforce**.
6. Click **Create**.

---

### 3. Publish 5 Valid Transaction Messages
1. Click your topic, then **Publish message**.
2. Enter valid JSON or binary data matching the schema (all required fields, correct types).
3. Publish 5 different messages.
4. Log each successful publish in your `test_report.log`.

---

### 4. Publish a Message with an Invalid Data Type
1. Try publishing a message with an invalid type (e.g., `amount` as a string).
2. Confirm the message is rejected (error shown in console).
3. Log the error/result in your `test_report.log`.

---

### 5. Create a Subscription and Pull All Valid Messages
1. In your topic, click **Create subscription**.
2. Name the subscription (e.g., `transaction-sub-<student_id>`).
3. Use default settings and create.
4. Click the subscription, then **Pull** to view received messages.
5. Log the received messages in your `test_report.log`.

---

**Tip:** Log every action and result for evaluation. If you get stuck, use the Cloud Console help or ask your instructor.

# GCP Pub/Sub Case Study 1: IoT Device Data Ingestion

## Scenario
You are part of a smart city project. Your team is responsible for ingesting sensor data from thousands of IoT devices into Google Cloud Pub/Sub. To ensure data quality, you must enforce a schema on the incoming messages.

## Tasks
1. **Create a Pub/Sub schema** (AVRO or Protocol Buffer) for IoT sensor data (fields: device_id, timestamp, temperature, humidity).
2. **Create a Pub/Sub topic** and associate it with the schema to enforce message validation.
3. **Publish at least 3 valid messages** to the topic using the schema.
4. **Attempt to publish an invalid message** (e.g., missing a required field) and verify it is rejected.
5. **Create a subscription** and pull messages, logging the received data.

## Verification
- The evaluator will check for schema creation, topic association, valid/invalid message handling, and subscription delivery.

## Notes
- Use OIDC authentication (no static keys).
- All actions and results must be logged to `test_report.log`.
- Do not delete or overwrite resources from other students.

---
See `solution_guide.md` for step-by-step instructions and `pre_setup.md` for instructor setup.

# IoT Sensor Data ETL Evaluator (BigQuery + Dataflow + Spanner)

## Case Study: IoT Sensor Data ETL

### Scenario
You are a data engineer for a smart city project. IoT sensors across the city send temperature and humidity readings to a shared BigQuery table (`iot_shared.sensor_raw`). Your job is to process this data, clean and aggregate it using Dataflow, and load the summarized results into a Cloud Spanner database (`iot-shared-instance`, database: `iot_shared_db`) for analytics.

### Task Overview
1. **Extract**: Read raw sensor data from the shared BigQuery table.
2. **Transform**: Use Dataflow to:
   - Filter out invalid readings (e.g., temperature < -50 or > 60).
   - Aggregate average temperature and humidity per sensor per day.
3. **Load**: Write the aggregated results to your own table in the shared Spanner database (table name: `sensor_summary_{student_id}`).

### Student Deliverables
- A Dataflow job (Python or Java) that performs the ETL as described.
- The output table in Spanner must have columns: `sensor_id`, `reading_date`, `avg_temp`, `avg_humidity`.
- The evaluator will check:
  - The Dataflow job ran and completed.
  - The output table exists in Spanner, with correct schema.
  - The data matches expected aggregates from the input.

### Shared Resources (Instructor Pre-Setup)
- BigQuery dataset/table: `iot_shared.sensor_raw` (with sample sensor data)
- Dataflow template or permissions for students to run jobs
- Spanner instance: `iot-shared-instance`
- Spanner database: `iot_shared_db`

---

## How to Run the Evaluator
- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

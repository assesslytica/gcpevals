# Dataproc Shared Cluster ETL Evaluator: Log Analytics

## Case Study: Log Analytics with Dataproc (Shared Cluster)

### Scenario
You are a data engineer for a large organization. Application logs are collected daily in a shared Cloud Storage bucket (`gs://logs-shared-bucket/app_logs/`). Your job is to process these logs using a shared Dataproc cluster (`dataproc-shared-cluster`), aggregate error counts per application, and write the results to a shared BigQuery dataset (`logs_shared.analytics_results`).

### Task Overview
1. **Extract**: Read raw log files from the shared Cloud Storage bucket.
2. **Transform**: Use a PySpark job on the shared Dataproc cluster to:
   - Parse log lines and extract application name and error type.
   - Aggregate error counts per application.
3. **Load**: Write the aggregated results to your own table in the shared BigQuery dataset (table name: `error_summary_{student_id}`).

### Student Deliverables
- A PySpark job that performs the ETL as described.
- The output table in BigQuery must have columns: `app_name`, `error_type`, `error_count`.
- The evaluator will check:
  - The Dataproc job ran and completed.
  - The output table exists in BigQuery, with correct schema.
  - The data matches expected aggregates from the input.

### Shared Resources (Instructor Pre-Setup)
- Cloud Storage bucket: `gs://logs-shared-bucket/app_logs/` (with sample log files)
- Dataproc cluster: `dataproc-shared-cluster`
- BigQuery dataset: `logs_shared.analytics_results`

---

## How to Run the Evaluator
- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

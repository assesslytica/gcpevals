# Healthcare Patient Vitals ETL Evaluator (BigQuery + Dataflow + Spanner)

## Case Study: Healthcare Patient Vitals ETL

### Scenario
You are a data engineer for a hospital network. Patient vital signs are collected in a shared BigQuery table (`health_shared.vitals_raw`). Your job is to process this data, clean and aggregate it using Dataflow, and load the summarized results into a Cloud Spanner database (`health-shared-instance`, database: `health_shared_db`) for clinical analytics.

### Task Overview
1. **Extract**: Read raw vitals data from the shared BigQuery table.
2. **Transform**: Use Dataflow to:
   - Filter out readings with missing patient IDs or impossible values (e.g., heart rate < 30 or > 220).
   - Aggregate average heart rate and blood pressure per patient per day.
3. **Load**: Write the aggregated results to your own table in the shared Spanner database (table name: `vitals_summary_{student_id}`).

### Student Deliverables
- A Dataflow job (Python or Java) that performs the ETL as described.
- The output table in Spanner must have columns: `patient_id`, `vital_date`, `avg_heart_rate`, `avg_bp`.
- The evaluator will check:
  - The Dataflow job ran and completed.
  - The output table exists in Spanner, with correct schema.
  - The data matches expected aggregates from the input.

### Shared Resources (Instructor Pre-Setup)
- BigQuery dataset/table: `health_shared.vitals_raw` (with sample vitals data)
- Dataflow template or permissions for students to run jobs
- Spanner instance: `health-shared-instance`
- Spanner database: `health_shared_db`

---

## How to Run the Evaluator
- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

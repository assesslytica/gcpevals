# E-Commerce Orders ETL Evaluator (BigQuery + Dataflow + Spanner)

## Case Study: E-Commerce Orders ETL

### Scenario
You are a data engineer for an e-commerce company. Customer orders are collected in a shared BigQuery table (`ecom_shared.orders_raw`). Your job is to process this data, clean and aggregate it using Dataflow, and load the summarized results into a Cloud Spanner database (`ecom-shared-instance`, database: `ecom_shared_db`) for business analytics.

### Task Overview
1. **Extract**: Read raw order data from the shared BigQuery table.
2. **Transform**: Use Dataflow to:
   - Filter out orders with missing or invalid customer IDs.
   - Aggregate total order value per customer per month.
3. **Load**: Write the aggregated results to your own table in the shared Spanner database (table name: `order_summary_{student_id}`).

### Student Deliverables
- A Dataflow job (Python or Java) that performs the ETL as described.
- The output table in Spanner must have columns: `customer_id`, `order_month`, `total_value`.
- The evaluator will check:
  - The Dataflow job ran and completed.
  - The output table exists in Spanner, with correct schema.
  - The data matches expected aggregates from the input.

### Shared Resources (Instructor Pre-Setup)
- BigQuery dataset/table: `ecom_shared.orders_raw` (with sample order data)
- Dataflow template or permissions for students to run jobs
- Spanner instance: `ecom-shared-instance`
- Spanner database: `ecom_shared_db`

---

## How to Run the Evaluator
- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

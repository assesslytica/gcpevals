# Retail Sales Data ETL Evaluator (BigQuery + Dataflow + Spanner)

## Case Study: Retail Sales Data ETL

### Scenario

You are a data engineer at a retail company. The company collects daily sales transactions in a BigQuery table (`retail_shared.sales_raw`). Your job is to process this data, clean and aggregate it using Dataflow, and load the summarized results into a Cloud Spanner database (`retail-shared-instance`, database: `retail_shared_db`) for downstream analytics.

### Task Overview

1. **Extract**: Read raw sales data from the shared BigQuery table.
2. **Transform**: Use Dataflow to:
   - Filter out invalid transactions (e.g., negative amounts).
   - Aggregate total sales per store and per day.
3. **Load**: Write the aggregated results to your own table in the shared Spanner database (table name: `sales_summary_{student_id}`).

### Student Deliverables

- A Dataflow job (Python or Java) that performs the ETL as described.
- The output table in Spanner must have columns: `store_id`, `sale_date`, `total_sales`.
- The evaluator will check:
  - The Dataflow job ran and completed.
  - The output table exists in Spanner, with correct schema.
  - The data matches expected aggregates from the input.

### Shared Resources (Instructor Pre-Setup)

- BigQuery dataset/table: `retail_shared.sales_raw` (with sample sales data)
- Dataflow template or permissions for students to run jobs
- Spanner instance: `retail-shared-instance`
- Spanner database: `retail_shared_db`

---

---

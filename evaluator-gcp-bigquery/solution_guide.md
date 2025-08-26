# Google Cloud BigQuery: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the BigQuery evaluator, from GCP login to running the workflow. It includes both Console and CLI/SQL instructions, IAM setup, troubleshooting, and tips.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable BigQuery API
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for **BigQuery API** and click **Enable**.

## 3. Create a BigQuery Dataset
- Go to **BigQuery** in the left menu.
- Click your project name, then click **Create Dataset**.
- Dataset ID: `bq_dataset_<student_id>` (replace `<student_id>` with your ID, e.g., `bq_dataset_tester1`).
- Data location: `asia-south1` (unless otherwise instructed).
- Click **Create Dataset**.

## 4. Create a Table and Schema
- In your dataset, click **Create Table**.
- Table name: `sales_data_<student_id>` (e.g., `sales_data_tester1`).
- Schema:
  - `id` (INT64, required)
  - `sale_date` (DATE, required)
  - `amount` (FLOAT64, required)
  - `region` (STRING, required)
- Click **Create Table**.

## 5. Insert Sample Data
- In the BigQuery Console, click your table, then click **Insert** > **Insert rows**.
- Insert at least 3 rows, for example:
  - id: 1, sale_date: 2023-01-01, amount: 100.5, region: West
  - id: 2, sale_date: 2023-01-02, amount: 200.0, region: East
  - id: 3, sale_date: 2023-01-03, amount: 150.75, region: North

### Option: Using SQL
You can also use the BigQuery Console or CLI to run:
```sql
INSERT INTO `bq_dataset_<student_id>.sales_data_<student_id>` (id, sale_date, amount, region) VALUES
  (1, '2023-01-01', 100.5, 'West'),
  (2, '2023-01-02', 200.0, 'East'),
  (3, '2023-01-03', 150.75, 'North');
```

## 6. Grant Access to Evaluator Service Account
- Go to **IAM & Admin > IAM** in the Cloud Console.
- Click **Grant Access**.
- Add the evaluator's service account email (provided by your instructor or workflow).
- Assign the **BigQuery Data Viewer** role for your project or dataset.
- Click **Save**.

## 7. Run the Evaluator Workflow
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP BigQuery Student Resources** workflow.
- Enter your `<student_id>` and run the workflow.
- Download and review the `test_report.log` artifact for results.

## Troubleshooting & Tips
- **Dataset/Table Not Found:** Double-check names and region.
- **Insufficient Rows:** Ensure at least 3 rows with all required columns.
- **Permission Errors:** Confirm the evaluator service account has BigQuery Data Viewer access.
- **Workflow Fails:** Check the Actions log for Python errors or missing environment variables.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

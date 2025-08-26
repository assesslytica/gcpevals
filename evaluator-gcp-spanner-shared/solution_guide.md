# Google Cloud Spanner Shared Instance: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the Spanner shared instance evaluator, from GCP login to running the workflow. It includes Console, CLI, SQL, IAM setup, troubleshooting, and tips.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable Spanner API
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for **Spanner API** and click **Enable**.

## 3. Review Shared Resources
- Spanner instance: `spanner-shared-instance`
- Spanner database: `spanner_shared_db`
- (See `pre_setup.md` for details)

## 4. Create Your Table
- In the shared database, create a table named `sales_data_<student_id>` with columns:
  - `id` (INT64, PRIMARY KEY)
  - `sale_date` (DATE)
  - `amount` (FLOAT64)
  - `region` (STRING(50))
- Example DDL:
  ```sql
  CREATE TABLE sales_data_<student_id> (
    id INT64 NOT NULL,
    sale_date DATE,
    amount FLOAT64,
    region STRING(50),
  ) PRIMARY KEY(id);
  ```

## 5. Insert Sample Data
- Insert at least 3 rows into your table with realistic values.
- Example:
  ```sql
  INSERT INTO sales_data_<student_id> (id, sale_date, amount, region) VALUES
    (1, '2023-01-01', 100.5, 'West'),
    (2, '2023-01-02', 200.0, 'East'),
    (3, '2023-01-03', 150.75, 'North');
  ```

## 6. Write and Run a Query
- Write a SQL query to calculate total sales per region from your table:
  ```sql
  SELECT region, SUM(amount) AS total_sales
  FROM sales_data_<student_id>
  GROUP BY region;
  ```
- Run the query in the Spanner Console or CLI and save the output.


## 7. Verify Your Work
- Ensure your table exists, has the correct schema, contains at least 3 rows, and your query returns the expected result.

## 8. Run the Evaluator Workflow
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP Spanner Shared Instance Student Resources** workflow.
- Enter your `<student_id>` and run the workflow.
- Download and review the `test_report.log` artifact for results.

---

## OIDC Access
The evaluator workflow uses OIDC authentication and will have access to your table as long as the GitHub Actions identity has the necessary permissions on the shared Spanner instance/database. No explicit grant to a service account is required.

## Troubleshooting & Tips
- **Table Not Found:** Double-check table name and database.
- **Insufficient Rows:** Ensure at least 3 rows with all required columns.
- **Permission Errors:** Confirm the evaluator service account has read access.
- **Workflow Fails:** Check the Actions log for Python errors or missing environment variables.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

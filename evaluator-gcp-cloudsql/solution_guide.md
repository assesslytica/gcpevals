
# Cloud SQL Data Engineering: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the Cloud SQL evaluator, starting from GCP login to final verification.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable Cloud SQL Admin API
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for **Cloud SQL Admin API** and click **Enable**.

## 3. Create a Cloud SQL Instance
- Go to **SQL** in the left menu.
- Click **Create Instance** > **MySQL**.
- Set the instance name to: `sql-instance-<student_id>` (replace `<student_id>` with your ID, e.g., `sql-instance-tester1`).
- Set the region to `asia-south1`.
- Choose MySQL 8.0.
- Enable **Public IP**.
- Set the root password to: `X9085565r` (required for evaluator).
- Click **Create Instance** and wait for provisioning.

## 4. Create a Database
- In your instance, go to the **Databases** tab.
- Click **Create database**.
- Name: `studentdb_<student_id>` (e.g., `studentdb_tester1`).
- Click **Create**.

## 5. Create a Table and Insert Data
- Go to the **Users** tab and ensure the root user exists.
- Click **Connect using Cloud Shell** or use a MySQL client with the public IP, root user, and password `X9085565r`.
- Run the following SQL (replace `<student_id>`):

```sql
USE studentdb_<student_id>;
CREATE TABLE sales_data_<student_id> (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sale_date DATE,
  amount FLOAT,
  region VARCHAR(50)
);
INSERT INTO sales_data_<student_id> (sale_date, amount, region) VALUES
  ('2023-01-01', 100.5, 'West'),
  ('2023-01-02', 200.0, 'East'),
  ('2023-01-03', 150.75, 'North');
```

## 6. Create a User and Grant Privileges
```sql
CREATE USER 'studentuser_<student_id>'@'%' IDENTIFIED BY 'TestUserPass123!';
GRANT SELECT, INSERT ON studentdb_<student_id>.sales_data_<student_id> TO 'studentuser_<student_id>'@'%';
FLUSH PRIVILEGES;
```

## 7. Verify Your Work
- Double-check all names and values match the instructions.
- Make sure the root password is `X9085565r`.
- Ensure at least 3 rows are present in the table.
- Ensure the user has SELECT and INSERT privileges.

## 8. Run the Evaluator Workflow
- Push your changes if needed.
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP Cloud SQL Student Resources** workflow.
- Click **Run workflow**, enter your `<student_id>`, and start the workflow.
- Download and review the `test_report.log` artifact for results.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

- Replace `<student_id>` with your test value everywhere.
- Use the Cloud Console or MySQL client to run these commands.
- The evaluator workflow will PASS if all steps are completed as above.

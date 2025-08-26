
# Google Cloud Bigtable: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the Bigtable evaluator, from GCP login to running the workflow. It includes both Console and CLI/Python instructions, IAM setup, troubleshooting, and tips.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable Bigtable Admin API
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for **Bigtable Admin API** and click **Enable**.

## 3. Create a Bigtable Instance
- In the left menu, go to **Bigtable** > **Instances**.
- Click **Create Instance**.
- Set the instance name and ID to: `bigtable-instance-<student_id>` (replace `<student_id>` with your ID, e.g., `bigtable-instance-tester1`).
- Set the display name as you like.
- Choose **Development** type (sufficient for this test).
- Set the region to `asia-south1` (or as instructed).
- Click **Create** and wait for provisioning.

## 4. Create a Table and Column Family
- In your instance, click **Create Table**.
- Table name: `sales_table_<student_id>` (e.g., `sales_table_tester1`).
- Initial column family: `cf1`
- Click **Create**.

## 5. Insert Sample Data
You can use the **cbt** CLI tool, Python, or Cloud Shell. Here are two options:

### Option A: Using cbt CLI
1. [Install cbt](https://cloud.google.com/bigtable/docs/cbt-overview#install)
2. Authenticate: `gcloud auth application-default login`
3. Set up cbt `.cbtrc` config:
   ```
   project = <your_project_id>
   instance = bigtable-instance-<student_id>
   ```
4. Insert rows:
   ```sh
   cbt set sales_table_<student_id> row1 cf1:date=2023-01-01 cf1:amount=100.5 cf1:region=West
   cbt set sales_table_<student_id> row2 cf1:date=2023-01-02 cf1:amount=200.0 cf1:region=East
   cbt set sales_table_<student_id> row3 cf1:date=2023-01-03 cf1:amount=150.75 cf1:region=North
   ```

### Option B: Using Python
```python
from google.cloud import bigtable
project = '<your_project_id>'
instance_id = 'bigtable-instance-<student_id>'
table_id = 'sales_table_<student_id>'
client = bigtable.Client(project=project, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)
rows = []
for i, (date, amount, region) in enumerate([
	('2023-01-01', 100.5, 'West'),
	('2023-01-02', 200.0, 'East'),
	('2023-01-03', 150.75, 'North')
]):
	row_key = f'row{i+1}'.encode()
	row = table.direct_row(row_key)
	row.set_cell('cf1', 'date', date)
	row.set_cell('cf1', 'amount', str(amount))
	row.set_cell('cf1', 'region', region)
	rows.append(row)
table.mutate_rows(rows)
```

## 6. Grant Access to Evaluator Service Account
- Go to **IAM & Admin > IAM** in the Cloud Console.
- Click **Grant Access**.
- Add the evaluator's service account email (provided by your instructor or workflow).
- Assign the **Bigtable Reader** role for your project or instance.
- Click **Save**.

## 7. Run the Evaluator Workflow
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP Bigtable Student Resources** workflow.
- Enter your `<student_id>` and run the workflow.
- Download and review the `test_report.log` artifact for results.

## Troubleshooting & Tips
- **Instance/Table Not Found:** Double-check names and region.
- **Insufficient Rows:** Ensure at least 3 rows, each with `date`, `amount`, and `region` in `cf1`.
- **Permission Errors:** Confirm the evaluator service account has Bigtable Reader access.
- **Workflow Fails:** Check the Actions log for Python errors or missing environment variables.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

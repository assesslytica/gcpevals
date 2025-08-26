# Google Cloud Dataproc: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the Dataproc evaluator, from GCP login to running the workflow. It includes Console, CLI, PySpark, IAM setup, troubleshooting, and tips.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable Dataproc and Storage APIs
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for **Dataproc API** and **Cloud Storage API** and click **Enable** for both.

## 3. Create a Cloud Storage Bucket
- Go to **Storage** in the left menu.
- Click **Create Bucket**.
- Name: `dataproc-bucket-<student_id>` (replace `<student_id>` with your ID, e.g., `dataproc-bucket-tester1`).
- Location: `asia-south1` (unless otherwise instructed).
- Click **Create**.

## 4. Upload Sample Data
- Create a CSV file named `sales_data_<student_id>.csv` with at least 3 rows and columns: `id,sale_date,amount,region`
- Example:
  ```csv
  id,sale_date,amount,region
  1,2023-01-01,100.5,West
  2,2023-01-02,200.0,East
  3,2023-01-03,150.75,North
  ```
- Upload this file to your bucket.

## 5. Create a Dataproc Cluster
- Go to **Dataproc** in the left menu.
- Click **Create Cluster**.
- Name: `dataproc-cluster-<student_id>`
- Region: `asia-south1`
- Cluster type: Single node (1 master, 0 workers)
- Click **Create**.

## 6. Submit a PySpark Job
- Create a PySpark script (e.g., `job_<student_id>.py`) with the following logic:
  - Read the CSV from the bucket
  - Calculate total sales per region
  - Write the result to `output_<student_id>.csv` in the same bucket
- Example PySpark code:
  ```python
  import sys
  from pyspark.sql import SparkSession
  spark = SparkSession.builder.appName('SalesAgg').getOrCreate()
  input_path = sys.argv[1]
  output_path = sys.argv[2]
  df = spark.read.csv(input_path, header=True, inferSchema=True)
  result = df.groupBy('region').sum('amount').withColumnRenamed('sum(amount)', 'total_sales')
  result.coalesce(1).write.csv(output_path, header=True, mode='overwrite')
  spark.stop()
  ```
- Upload the script to the bucket or your local machine.
- Submit the job:
  ```sh
  gcloud dataproc jobs submit pyspark job_<student_id>.py \
    --cluster=dataproc-cluster-<student_id> \
    --region=asia-south1 \
    -- \
    gs://dataproc-bucket-<student_id>/sales_data_<student_id>.csv \
    gs://dataproc-bucket-<student_id>/output_<student_id>.csv
  ```

## 7. Verify Output
- In your bucket, check for `output_<student_id>.csv` (it may be in a subfolder).
- Download and open the file. It should contain total sales per region.

## 8. Run the Evaluator Workflow
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP Dataproc Student Resources** workflow.
- Enter your `<student_id>` and run the workflow.
- Download and review the `test_report.log` artifact for results.

## Troubleshooting & Tips
- **Cluster/File Not Found:** Double-check names and region.
- **PySpark Errors:** Check job logs in Dataproc.
- **Output Missing:** Ensure your script writes to the correct bucket and path.
- **Workflow Fails:** Check the Actions log for Python errors or missing environment variables.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

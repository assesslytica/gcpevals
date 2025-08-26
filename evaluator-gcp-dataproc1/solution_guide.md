# Solution Guide: Log Analytics with Dataproc (Shared Cluster)

This guide will walk you through the ETL process step by step, with explanations and sample commands. No prior GCP experience is required.

---

## 1. Explore the Input Data in Cloud Storage
1. Go to the [Cloud Storage Console](https://console.cloud.google.com/storage/browser).
2. Find the bucket `logs-shared-bucket` and folder `app_logs/`.
3. Download or preview a sample log file to understand its format (e.g., JSON or plain text lines).

---

## 2. Write Your PySpark ETL Job
You can use PySpark to process the logs. Below is a sample structure.

### a. Install Required Packages (locally for testing)
```bash
pip install pyspark google-cloud-bigquery
```

### b. Sample PySpark Job (log_etl.py)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract, count

spark = SparkSession.builder.appName('LogAnalytics').getOrCreate()
logs = spark.read.text('gs://logs-shared-bucket/app_logs/*.log')

# Example: Extract app_name and error_type from log lines
logs_parsed = logs.withColumn('app_name', regexp_extract('value', r'app=(\w+)', 1)) \
    .withColumn('error_type', regexp_extract('value', r'error=(\w+)', 1))

error_counts = logs_parsed.groupBy('app_name', 'error_type').agg(count('*').alias('error_count'))

# Write to BigQuery
error_counts.write.format('bigquery') \
    .option('table', 'logs_shared.analytics_results.error_summary_{student_id}') \
    .option('temporaryGcsBucket', 'logs-shared-bucket') \
    .save()
```
**Note:** Replace `{student_id}` with your actual ID in the output table name.

---

## 3. Submit Your Job to Dataproc
1. Package your script and dependencies (if any).
2. Submit the job using the [Dataproc Jobs UI](https://console.cloud.google.com/dataproc/jobs) or with gcloud:
   ```bash
   gcloud dataproc jobs submit pyspark log_etl.py \
     --cluster=dataproc-shared-cluster \
     --region=YOUR_REGION
   ```
3. Monitor your job in the Dataproc Jobs UI.

---

## 4. Verify Your Results in BigQuery
1. Go to the [BigQuery Console](https://console.cloud.google.com/bigquery).
2. Query your output table:
   ```sql
   SELECT * FROM logs_shared.analytics_results.error_summary_{student_id} LIMIT 10;
   ```
3. Check that the data matches the expected error aggregates from the logs.

---

## 5. Clean Up (Optional)
After evaluation, you may delete your output table to keep the shared dataset tidy.

---

## Tips
- Use OIDC for all authentication (no service account key needed).
- If you get permission errors, check with your instructor that your account is added and OIDC is set up.
- Ask for help if you get stuck—this is a learning exercise!

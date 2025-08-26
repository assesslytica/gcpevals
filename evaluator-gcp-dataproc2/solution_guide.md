# Solution Guide: Retail Transaction Analytics with Dataproc (Shared Cluster)

This guide will walk you through the ETL process step by step, with explanations and sample commands. No prior GCP experience is required.

---

## 1. Explore the Input Data in Cloud Storage
1. Go to the [Cloud Storage Console](https://console.cloud.google.com/storage/browser).
2. Find the bucket `retail-shared-bucket` and folder `transactions/`.
3. Download or preview a sample CSV file to understand its format (e.g., columns: store_id, sale_date, amount).

---

## 2. Write Your PySpark ETL Job
You can use PySpark to process the transactions. Below is a sample structure.

### a. Install Required Packages (locally for testing)
```bash
pip install pyspark google-cloud-bigquery
```

### b. Sample PySpark Job (retail_etl.py)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

spark = SparkSession.builder.appName('RetailAnalytics').getOrCreate()
data = spark.read.csv('gs://retail-shared-bucket/transactions/*.csv', header=True, inferSchema=True)

sales_summary = data.groupBy('store_id', 'sale_date').agg(_sum('amount').alias('total_sales'))

# Write to BigQuery
sales_summary.write.format('bigquery') \
    .option('table', 'retail_shared.analytics_results.sales_summary_{student_id}') \
    .option('temporaryGcsBucket', 'retail-shared-bucket') \
    .save()
```
**Note:** Replace `{student_id}` with your actual ID in the output table name.

---

## 3. Submit Your Job to Dataproc
1. Package your script and dependencies (if any).
2. Submit the job using the [Dataproc Jobs UI](https://console.cloud.google.com/dataproc/jobs) or with gcloud:
   ```bash
   gcloud dataproc jobs submit pyspark retail_etl.py \
     --cluster=dataproc-shared-cluster \
     --region=YOUR_REGION
   ```
3. Monitor your job in the Dataproc Jobs UI.

---

## 4. Verify Your Results in BigQuery
1. Go to the [BigQuery Console](https://console.cloud.google.com/bigquery).
2. Query your output table:
   ```sql
   SELECT * FROM retail_shared.analytics_results.sales_summary_{student_id} LIMIT 10;
   ```
3. Check that the data matches the expected sales aggregates from the input.

---

## 5. Clean Up (Optional)
After evaluation, you may delete your output table to keep the shared dataset tidy.

---

## Tips
- Use OIDC for all authentication (no service account key needed).
- If you get permission errors, check with your instructor that your account is added and OIDC is set up.
- Ask for help if you get stuck—this is a learning exercise!

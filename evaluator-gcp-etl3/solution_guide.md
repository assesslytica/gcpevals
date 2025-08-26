# Solution Guide: E-Commerce Orders ETL

This guide will walk you through the ETL process step by step, with explanations and sample commands. No prior GCP experience is required.

---

## 1. Explore the Input Data in BigQuery
1. Go to the [BigQuery Console](https://console.cloud.google.com/bigquery).
2. In the Explorer panel, find the dataset `ecom_shared` and table `orders_raw`.
3. Click the table to view its schema and preview the data.
   - Typical columns: `order_id` (STRING), `customer_id` (STRING), `order_date` (DATE), `order_value` (FLOAT)
4. (Optional) Run a sample query:
   ```sql
   SELECT * FROM `ecom_shared.orders_raw` LIMIT 10;
   ```

---

## 2. Write Your Dataflow ETL Pipeline
You can use Python (Apache Beam) or Java. Below is a Python example using Apache Beam.

### a. Install Required Packages
```bash
pip install apache-beam[gcp] google-cloud-spanner
```

### b. Sample Python Pipeline (etl_pipeline.py)
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class FilterAndAggregate(beam.DoFn):
    def process(self, element):
        if not element['customer_id']:
            return
        key = (element['customer_id'], element['order_date'][:7])  # YYYY-MM
        yield (key, element['order_value'])

def run():
    options = PipelineOptions(
        project='YOUR_PROJECT_ID',
        region='YOUR_REGION',
        temp_location='gs://YOUR_BUCKET/temp',
        runner='DataflowRunner'
    )
    with beam.Pipeline(options=options) as p:
        rows = (
            p
            | 'ReadFromBigQuery' >> beam.io.ReadFromBigQuery(
                table='ecom_shared.orders_raw',
                use_standard_sql=True)
            | 'FilterAndAggregate' >> beam.ParDo(FilterAndAggregate())
            | 'SumOrders' >> beam.CombinePerKey(sum)
        )
        def to_dict(kv):
            (customer_id, order_month), total_value = kv
            return {
                'customer_id': customer_id,
                'order_month': order_month,
                'total_value': total_value
            }
        rows | 'FormatForSpanner' >> beam.Map(to_dict)
        # TODO: Write to Spanner using a custom sink or Dataflow connector

if __name__ == '__main__':
    run()
```

**Note:** Replace `YOUR_PROJECT_ID`, `YOUR_REGION`, and `YOUR_BUCKET` with your actual GCP project, region, and a GCS bucket you have access to.

---

## 3. Create the Output Table in Spanner
1. Go to the [Spanner Console](https://console.cloud.google.com/spanner).
2. Select the instance `ecom-shared-instance` and database `ecom_shared_db`.
3. Click **Create Table** and use the following DDL (replace `{student_id}` with your ID):
   ```sql
   CREATE TABLE order_summary_{student_id} (
     customer_id STRING(64) NOT NULL,
     order_month STRING(7) NOT NULL,
     total_value FLOAT64
   ) PRIMARY KEY (customer_id, order_month);
   ```

---

## 4. Run Your Dataflow Pipeline
1. Submit your pipeline to Dataflow:
   ```bash
   python etl_pipeline.py \
     --project=YOUR_PROJECT_ID \
     --region=YOUR_REGION \
     --runner=DataflowRunner \
     --temp_location=gs://YOUR_BUCKET/temp
   ```
2. Monitor your job in the [Dataflow Console](https://console.cloud.google.com/dataflow).
3. Make sure the job completes successfully.

---

## 5. Verify Your Results
1. In Spanner, query your output table:
   ```sql
   SELECT * FROM order_summary_{student_id} LIMIT 10;
   ```
2. Check that the data matches the expected aggregates from the input.

---

## 6. Clean Up (Optional)
After evaluation, you may delete your output table to keep the shared database tidy.

---

## Tips
- Use OIDC for all authentication (no service account key needed).
- If you get permission errors, check with your instructor that your account is added and OIDC is set up.
- Ask for help if you get stuck—this is a learning exercise!

# Google Cloud Dataflow: Complete Step-by-Step Solution Guide

This guide will help you complete all required tasks for the Dataflow evaluator, from GCP login to running the workflow. It includes Console, CLI, Python, IAM setup, troubleshooting, and tips.

---

## 1. Log in to Google Cloud Console
- Go to https://console.cloud.google.com/
- Log in with your Google account.
- Select or create a project for your work.

## 2. Enable Dataflow, Pub/Sub, and BigQuery APIs
- In the Cloud Console, go to **APIs & Services > Library**.
- Search for and enable:
  - Dataflow API
  - Pub/Sub API
  - BigQuery API

## 3. Review Shared Resources
- Pub/Sub topic: `dataflow-shared-topic`
- BigQuery dataset: `dataflow_shared`
- (See `pre_setup.md` for details)

## 4. Write and Deploy a Dataflow Pipeline
- Use Apache Beam (Python) to create a pipeline that:
  - Reads messages from the shared Pub/Sub topic
  - Parses each message (e.g., JSON)
  - Extracts fields: `id`, `sale_date`, `amount`, `region`
  - Writes the results to your BigQuery table: `dataflow_shared.dataflow_output_<student_id>`
- Example pipeline code (Python):
  ```python
  import apache_beam as beam
  from apache_beam.options.pipeline_options import PipelineOptions
  import json

  class ParseMessage(beam.DoFn):
      def process(self, element):
          row = json.loads(element.decode('utf-8'))
          yield {
              'id': row['id'],
              'sale_date': row['sale_date'],
              'amount': float(row['amount']),
              'region': row['region']
          }

  options = PipelineOptions([
      '--runner=DataflowRunner',
      '--project=<your_project_id>',
      '--region=asia-south1',
      '--temp_location=gs://<your_temp_bucket>/temp'
  ])

  with beam.Pipeline(options=options) as p:
      (
          p
          | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(topic='projects/<your_project_id>/topics/dataflow-shared-topic')
          | 'Parse' >> beam.ParDo(ParseMessage())
          | 'WriteToBQ' >> beam.io.WriteToBigQuery(
                table='dataflow_shared.dataflow_output_<student_id>',
                schema='id:INTEGER,sale_date:STRING,amount:FLOAT,region:STRING',
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
      )
  ```
- Deploy the pipeline using the Dataflow Console or CLI.

## 5. Publish Test Messages
- Publish at least 3 JSON messages to the shared Pub/Sub topic. Example:
  ```json
  {"id": 1, "sale_date": "2023-01-01", "amount": 100.5, "region": "West"}
  {"id": 2, "sale_date": "2023-01-02", "amount": 200.0, "region": "East"}
  {"id": 3, "sale_date": "2023-01-03", "amount": 150.75, "region": "North"}
  ```
- Use the Console or `gcloud pubsub topics publish` command.

## 6. Verify Output
- In BigQuery, check your table `dataflow_shared.dataflow_output_<student_id>` for at least 3 rows with the expected data.

## 7. Run the Evaluator Workflow
- Go to the **Actions** tab in your GitHub repository.
- Select the **Evaluate GCP Dataflow Student Resources** workflow.
- Enter your `<student_id>` and run the workflow.
- Download and review the `test_report.log` artifact for results.

## Troubleshooting & Tips
- **Pipeline Not Running:** Check Dataflow job logs for errors.
- **No Data in Table:** Ensure your pipeline is running and messages are published to the correct topic.
- **Permission Errors:** Confirm you have access to the shared resources.
- **Workflow Fails:** Check the Actions log for Python errors or missing environment variables.

---

**If you follow these steps exactly, the evaluator will PASS all checks.**

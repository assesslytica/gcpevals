
# gcpevals

This repository contains a suite of automated GCP evaluator scenarios for classroom and lab use. Each evaluator is scenario-driven, OIDC-authenticated, and logs results for robust, scalable assessment.

## Evaluator Index

| Evaluator | Brief Objective |
|-----------|----------------|
| **BigQuery** | Create dataset, table, load data, and run aggregation queries in BigQuery. Tests schema, data loading, and SQL skills. |
| **Bigtable** | Provision Bigtable instance/table, load sample data, and configure access. Evaluates NoSQL modeling and GCP IAM. |
| **Cloud SQL** | Deploy Cloud SQL instance, create schema, load data, and set up user privileges. Assesses relational DB setup and access control. |
| **Cloud SQL Shared** | Use a shared Cloud SQL instance to create tables, insert data, run queries, and export results to Cloud Storage. Focuses on shared resource usage and analytics. |
| **Dataflow** | Build and deploy a Dataflow pipeline to process Pub/Sub messages and write results to BigQuery. Tests ETL and streaming concepts. |
| **Dataproc** | Create Dataproc cluster, run PySpark jobs on sample data in Cloud Storage, and verify output. Assesses distributed data processing. |
| **Dataproc Shared** | Use a shared Dataproc cluster and bucket to run PySpark jobs on your own input/output files. Focuses on collaborative resource use. |
| **ETL (Retail Sales)** | End-to-end ETL: extract from BigQuery, transform with Dataflow, and load to Spanner. Evaluates pipeline design and integration. |
| **Pub/Sub Case Study 1 (IoT)** | Enforce schema on IoT sensor data, publish/validate messages, and pull via subscription. Tests schema enforcement and real-time ingestion. |
| **Pub/Sub Case Study 2 (Finance)** | Enforce schema on financial transactions, validate message types, and pull via subscription. Focuses on compliance and data quality. |
| **Spanner Shared** | Use a shared Spanner instance to create tables, insert/query data, and verify analytics. Assesses distributed SQL and shared DB use. |
| **Storage Case Study 1 (Media)** | Upload, organize, secure, and share media files in GCS. Tests permissions, signed URLs, and file management. |
| **Storage Case Study 2 (Data Science)** | Collaborate on datasets in GCS: upload, set retention, share, download, and delete files. Focuses on secure, auditable storage use. |

---

**How to Use:**
- Each evaluator folder contains a README, solution guide, and pre-setup guide.
- Workflows use OIDC for secure, keyless authentication.
- All results are logged to `test_report.log` and downloadable as workflow artifacts.

**Update this index whenever a new evaluator is added.**

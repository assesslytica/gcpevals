
# Pre-Setup Guide: Retail Sales Data ETL Evaluator

This guide will help any instructor or admin configure all shared resources and authentication for the ETL evaluator, step by step. No prior GCP experience is required.

---

## 1. Enable Required APIs
1. Go to the [APIs & Services Library](https://console.cloud.google.com/apis/library) in your GCP project.
2. Enable these APIs:
	- Cloud BigQuery API
	- Cloud Dataflow API
	- Cloud Spanner API
	- IAM API

---

## 2. Set Up OIDC Authentication (One-Time)
1. In the [IAM & Admin > Workload Identity Federation](https://console.cloud.google.com/iam-admin/workload-identity-pools) section, create a Workload Identity Pool for your GitHub organization or repository.
2. Add a provider for GitHub Actions.
3. Create or select a service account for the evaluator workflow.
4. Grant this service account the following roles:
	- BigQuery Data Viewer
	- Dataflow Developer
	- Spanner Database Admin
5. Allow the Workload Identity Pool principal to impersonate the service account (add as a principal in the service account's permissions).
6. Add the OIDC provider and service account email as GitHub secrets in your repository:
	- `GCP_WORKLOAD_IDENTITY_PROVIDER`
	- `GCP_SERVICE_ACCOUNT_EMAIL`
7. **No service account key is needed.**

---

## 3. Create Shared BigQuery Dataset and Table
1. Go to the [BigQuery Console](https://console.cloud.google.com/bigquery).
2. Create a dataset named `retail_shared`.
3. In that dataset, create a table named `sales_raw` with columns:
	- `store_id` (STRING)
	- `sale_date` (DATE)
	- `amount` (FLOAT or NUMERIC)
4. Load sample sales data into the table (CSV or manual entry).
5. Grant read access to all student accounts or groups (add as BigQuery Data Viewer on the dataset).

---

## 4. Prepare Dataflow Permissions or Template
**Option 1:** Create a reusable Dataflow template for the ETL task and share the template path with students.

**Option 2:** Grant students permission to run Dataflow jobs in the project:
  - Add their emails or group as Dataflow Developer on the project.

---

## 5. Create Shared Spanner Instance and Database
1. Go to the [Spanner Console](https://console.cloud.google.com/spanner).
2. Create an instance named `retail-shared-instance` (1 node is enough for most classrooms).
3. In that instance, create a database named `retail_shared_db`.
4. Grant DDL/DML permissions to all student accounts or groups (Spanner Database Admin or User).

---

## 6. Communicate Resource Names and OIDC Setup
1. Share the following with students (add to README and solution guide):
	- BigQuery dataset/table: `retail_shared.sales_raw`
	- Spanner instance: `retail-shared-instance`
	- Spanner database: `retail_shared_db`
2. Remind students that authentication is handled via OIDC and no service account key is needed.

---

## 7. Quota/Cost Management
1. All students use the same shared resources.
2. Instructor can periodically clean up old tables/data in BigQuery and Spanner.

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**

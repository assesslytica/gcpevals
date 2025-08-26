# Pre-Setup Guide: Log Analytics with Dataproc (Shared Cluster)

This guide will help any instructor or admin configure all shared resources and authentication for the Dataproc evaluator, step by step. No prior GCP experience is required.

---

## 1. Enable Required APIs
1. Go to the [APIs & Services Library](https://console.cloud.google.com/apis/library) in your GCP project.
2. Enable these APIs:
   - Cloud Dataproc API
   - Cloud Storage API
   - Cloud BigQuery API
   - IAM API

---

## 2. Set Up OIDC Authentication (One-Time)
1. In the [IAM & Admin > Workload Identity Federation](https://console.cloud.google.com/iam-admin/workload-identity-pools) section, create a Workload Identity Pool for your GitHub organization or repository.
2. Add a provider for GitHub Actions.
3. Create or select a service account for the evaluator workflow.
4. Grant this service account the following roles:
   - Dataproc Editor
   - Storage Object Viewer
   - BigQuery Data Editor
5. Allow the Workload Identity Pool principal to impersonate the service account (add as a principal in the service account's permissions).
6. Add the OIDC provider and service account email as GitHub secrets in your repository:
   - `GCP_WORKLOAD_IDENTITY_PROVIDER`
   - `GCP_SERVICE_ACCOUNT_EMAIL`
7. **No service account key is needed.**

---

## 3. Create Shared Cloud Storage Bucket
1. Go to the [Cloud Storage Console](https://console.cloud.google.com/storage/browser).
2. Create a bucket named `logs-shared-bucket`.
3. Create a folder `app_logs/` and upload sample log files.
4. Grant read access to all student accounts or groups (Storage Object Viewer on the bucket).

---

## 4. Create Shared Dataproc Cluster
1. Go to the [Dataproc Clusters Console](https://console.cloud.google.com/dataproc/clusters).
2. Create a cluster named `dataproc-shared-cluster` (1-2 nodes is enough for most classrooms).
3. Grant job submission permissions to all student accounts or groups (Dataproc Editor on the project or cluster).

---

## 5. Create Shared BigQuery Dataset
1. Go to the [BigQuery Console](https://console.cloud.google.com/bigquery).
2. Create a dataset named `logs_shared`.
3. Create a table or allow students to create their own tables in `analytics_results`.
4. Grant Data Editor access to all student accounts or groups on the dataset.

---

## 6. Communicate Resource Names and OIDC Setup
- Share the following with students (add to README and solution guide):
  - Cloud Storage bucket: `gs://logs-shared-bucket/app_logs/`
  - Dataproc cluster: `dataproc-shared-cluster`
  - BigQuery dataset: `logs_shared.analytics_results`
- Remind students that authentication is handled via OIDC and no service account key is needed.

---

## 7. Quota/Cost Management
- All students use the same shared resources.
- Instructor can periodically clean up old tables/data in BigQuery and Cloud Storage.

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**

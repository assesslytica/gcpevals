# Pre-Setup Guide: Customer Feedback Analytics with Cloud SQL (Shared Instance)

This guide will help any instructor or admin configure all shared resources and authentication for the Cloud SQL evaluator, step by step. No prior GCP experience is required.

---

## 1. Enable Required APIs
1. Go to the [APIs & Services Library](https://console.cloud.google.com/apis/library) in your GCP project.
2. Enable these APIs:
   - Cloud SQL Admin API
   - Cloud Storage API
   - IAM API

---

## 2. Set Up OIDC Authentication (One-Time)
1. In the [IAM & Admin > Workload Identity Federation](https://console.cloud.google.com/iam-admin/workload-identity-pools) section, create a Workload Identity Pool for your GitHub organization or repository.
2. Add a provider for GitHub Actions.
3. Create or select a service account for the evaluator workflow.
4. Grant this service account the following roles:
   - Cloud SQL Client
   - Storage Object Viewer
   - Storage Object Creator
5. Allow the Workload Identity Pool principal to impersonate the service account (add as a principal in the service account's permissions).
6. Add the OIDC provider and service account email as GitHub secrets in your repository:
   - `GCP_WORKLOAD_IDENTITY_PROVIDER`
   - `GCP_SERVICE_ACCOUNT_EMAIL`
7. **No service account key is needed.**

---

## 3. Create Shared Cloud SQL Instance and Database
1. Go to the [Cloud SQL Console](https://console.cloud.google.com/sql/instances).
2. Create a PostgreSQL instance named `cloudsql-shared-instance` (smallest size is sufficient).
3. In that instance, create a database named `feedback_shared_db`.
4. Grant DDL/DML access to all student accounts or groups (Cloud SQL IAM authentication).

---

## 4. Communicate Resource Names and OIDC Setup
- Share the following with students (add to README and solution guide):
  - Cloud SQL instance: `cloudsql-shared-instance`
  - Database: `feedback_shared_db`
- Remind students that authentication is handled via OIDC/IAM and no service account key is needed.

---

## 5. Quota/Cost Management
- All students use the same shared resources.
- Instructor can periodically clean up old tables/data in the database and buckets.

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**

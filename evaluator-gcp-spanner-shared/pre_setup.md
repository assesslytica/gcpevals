

# Spanner Shared Instance Evaluator Pre-Setup (Instructor/Admin)

This guide will help any instructor or admin configure the shared Spanner resources and OIDC authentication, step by step. No prior GCP experience is required.

---

## 1. Enable Required APIs
1. Go to the [APIs & Services Library](https://console.cloud.google.com/apis/library) in your GCP project.
2. Enable these APIs:
	- Cloud Spanner API
	- IAM API

---

## 2. Set Up OIDC Authentication (One-Time)
1. In the [IAM & Admin > Workload Identity Federation](https://console.cloud.google.com/iam-admin/workload-identity-pools) section, create a Workload Identity Pool for your GitHub organization or repository.
2. Add a provider for GitHub Actions.
3. Create or select a service account for the evaluator workflow.
4. Grant this service account the following roles:
	- Spanner Database Admin (or Spanner Database User for limited DDL)
5. Allow the Workload Identity Pool principal to impersonate the service account (add as a principal in the service account's permissions).
6. Add the OIDC provider and service account email as GitHub secrets in your repository:
	- `GCP_WORKLOAD_IDENTITY_PROVIDER`
	- `GCP_SERVICE_ACCOUNT_EMAIL`
7. **No service account key is needed.**

---

## 3. Create a Shared Spanner Instance
1. Go to the [Spanner Console](https://console.cloud.google.com/spanner).
2. Click **Create Instance**.
3. Set the instance name and ID to: `spanner-shared-instance`.
4. Choose a region (e.g., `asia-south1`).
5. Choose 1 node (sufficient for most classrooms).
6. Click **Create**.

---

## 4. Create a Shared Spanner Database
1. In the new instance, click **Create Database**.
2. Set the database name to: `spanner_shared_db`.
3. Click **Create** (no need to add tables yet).

---

## 5. Grant Student Permissions
1. Go to [IAM & Admin > IAM](https://console.cloud.google.com/iam-admin/iam) in the Cloud Console.
2. Click **Grant Access**.
3. Add all student user emails (or a group) who will participate.
4. Assign the following roles:
	- `Cloud Spanner Database Admin` (for DDL/DML)
	- Or `Cloud Spanner Database User` (if you want to limit DDL)
5. Click **Save**.

---

## 6. Communicate Resource Names and OIDC Setup
1. Share the following with students (add to README and solution guide):
	- Spanner instance: `spanner-shared-instance`
	- Spanner database: `spanner_shared_db`
2. Remind students that authentication is handled via OIDC and no service account key is needed.

---

## 7. Quota/Cost Management
1. All students use the same shared resources.
2. Instructor can periodically clean up old tables/data in Spanner.

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**

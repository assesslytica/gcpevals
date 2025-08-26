# Pre-Setup Guide: GCP Pub/Sub Case Study 1 (Instructor)

## Purpose
Prepare a shared environment for IoT device data ingestion with schema enforcement.

## Steps
1. **Ensure Pub/Sub and Schema Registry APIs are enabled** in the project.
2. **Set up OIDC access** for GitHub Actions:
   - Create a Workload Identity Pool and Provider in GCP IAM.
   - Create a service account with Pub/Sub and schema admin permissions.
   - Grant the service account access to manage Pub/Sub and schemas.
   - Add the Workload Identity Provider and Service Account as GitHub secrets.
3. **Provide students with:**
   - Project ID
   - Their student ID
   - Instructions for naming topics/subscriptions uniquely
4. **Do not delete or overwrite resources from other students.**

---
See `README.md` for scenario and tasks. See `solution_guide.md` for student instructions.

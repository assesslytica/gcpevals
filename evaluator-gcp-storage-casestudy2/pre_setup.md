# Pre-Setup Guide: GCP Storage Case Study 2 (Instructor)

## Purpose
Prepare a shared GCS bucket for the data science collaboration scenario. Ensure OIDC access and correct permissions for students and collaborators.

## Steps
1. **Create the bucket** (if not already):
   - Name: `ds-collab-shared`
   - Location: Multi-region or region as needed
   - Default storage class: Standard

2. **Enable OIDC access** for GitHub Actions:
   - Set up a Workload Identity Pool and Provider in GCP IAM.
   - Create a service account with permissions for storage admin/object admin.
   - Grant the service account access to the bucket.
   - Add the Workload Identity Provider and Service Account as GitHub secrets.

3. **Provide students with:**
   - The bucket name
   - Their student ID
   - The collaborator’s email
   - The name of another student’s folder for download task

4. **Do not enable public access.**

---
See `README.md` for scenario and tasks. See `solution_guide.md` for student instructions.

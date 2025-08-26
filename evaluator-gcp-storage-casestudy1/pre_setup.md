# Pre-Setup Guide: GCP Storage Case Study 1 (Instructor)

## Purpose
Prepare a shared GCS bucket for the media asset management scenario. Ensure OIDC access and group permissions are ready for students.

## Steps
1. **Create the bucket** (if not already):
   - Name: `media-assets-shared`
   - Location: Multi-region or region as needed
   - Default storage class: Standard

2. **Enable OIDC access** for GitHub Actions:
   - Set up a Workload Identity Pool and Provider in GCP IAM.
   - Create a service account with permissions for storage admin/object admin.
   - Grant the service account access to the bucket.
   - Add the Workload Identity Provider and Service Account as GitHub secrets.

3. **Create a Google Group** for the student team (e.g., `media-team@example.com`).
   - Add all student emails to the group.

4. **Set bucket-level permissions** so the group has access to the bucket.

5. **Provide students with:**
   - The bucket name
   - The group email
   - Their student ID

6. **Do not enable public access.**

---
See `README.md` for scenario and tasks. See `solution_guide.md` for student instructions.

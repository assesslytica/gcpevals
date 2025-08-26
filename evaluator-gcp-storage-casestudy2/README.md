# GCP Storage Case Study 2: Data Science Collaboration

## Scenario
You are a data science student collaborating on a shared project. Your team uses a GCS bucket (`ds-collab-shared`) to exchange datasets and results. You must demonstrate secure, organized, and auditable use of Google Cloud Storage.

## Tasks
1. **Create** a folder in the `ds-collab-shared` bucket named after your student ID and upload a CSV dataset to it.
2. **Set a retention policy** of 7 days on your folder (or objects within it).
3. **Share** your uploaded file with a specific collaborator (email provided) and log the action.
4. **Download** a file from another student’s folder (name provided by instructor) and log the file size.
5. **Delete** a test file you uploaded and verify it is no longer present.

## Verification
- The evaluator will check for correct folder creation, upload, retention policy, sharing, download, and deletion.

## Notes
- Use OIDC authentication (no static keys).
- Do not modify or delete files from other students except as instructed.
- All actions must be logged to `test_report.log`.

---
See `solution_guide.md` for step-by-step instructions and `pre_setup.md` for instructor setup.

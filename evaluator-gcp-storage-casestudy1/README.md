# GCP Storage Case Study 1: Media Asset Management

## Scenario
You are a media intern at a digital agency. Your team uses a shared GCS bucket (`media-assets-shared`) to store, organize, and process client media files. You are tasked with demonstrating your ability to manage, secure, and process files in Google Cloud Storage.

## Tasks
1. **Upload** at least 3 image files (JPG/PNG) to the `media-assets-shared` bucket under a folder named after your student ID (e.g., `12345/`).
2. **Set object-level permissions** so only your team (group email provided) can access your uploaded files.
3. **List** all files in your folder and log their names and sizes.
4. **Move** one file to a subfolder called `archive/` within your student folder.
5. **Generate a signed URL** for one file and verify it works (log the URL and test result).

## Verification
- The evaluator will check for correct file upload, permissions, listing, file move, and signed URL functionality.

## Notes
- Use OIDC authentication (no static keys).
- Do not delete or overwrite files from other students.
- All actions must be logged to `test_report.log`.

---
See `solution_guide.md` for step-by-step instructions and `pre_setup.md` for instructor setup.

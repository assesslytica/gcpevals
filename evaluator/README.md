# Evaluator Workflow and Scripts

This folder contains:
- `workflows/`: GitHub Actions workflows for evaluating GCP resources.
- `scripts/`: Python scripts to check GCP bucket and Pub/Sub topic, and write a test report.

## Tasks
- Create a bucket `eval-<student_id>` in `asia-south1` with UBLA + Versioning
- Create a Pub/Sub topic `eval-topic-<student_id>`
- Evaluator checks those resources and writes `test_report.log` with PASS/FAIL and TOTAL_SCORE

See the respective subfolders for details.

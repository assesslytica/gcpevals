# GCP Dataflow Evaluator – Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All resources must be named using the convention: `<resource>_<student_id>` (replace `<student_id>` with your actual student ID).

### Tasks
1. **Write and deploy a Dataflow pipeline**
   - The pipeline must:
     - Read messages from the shared Pub/Sub topic (see `pre_setup.md` for topic name).
     - Transform each message (e.g., parse JSON, extract fields, compute a value).
     - Write the results to your own BigQuery table: `dataflow_output_<student_id>` in dataset `dataflow_shared`.

2. **Publish test messages**
   - Publish at least 3 test messages to the shared Pub/Sub topic (via Console or CLI).

3. **Verify output**
   - Ensure your BigQuery table contains at least 3 rows with the expected transformed data.

---

## Naming Convention
- BigQuery table: `dataflow_output_<student_id>` in dataset `dataflow_shared`.
- The evaluator will use the student ID input to check for the correct resources.

---

## Verification
- The evaluator workflow will check for the existence and configuration of your BigQuery table and data.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation, delete your BigQuery table. The shared Pub/Sub topic and dataset are managed by the instructor.

---

**See `solution_guide.md` for a full, step-by-step walkthrough.**

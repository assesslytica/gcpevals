# GCP Dataproc Evaluator – Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All resources must be named using the convention: `<resource>-<student_id>` (replace `<student_id>` with your actual student ID).

### Tasks
1. **Create a Dataproc cluster**
   - Name: `dataproc-cluster-<student_id>`
   - Region: `asia-south1` (unless otherwise instructed)
   - Single node (1 master, 0 workers) is sufficient for this test

2. **Upload a sample CSV file to Cloud Storage**
   - Bucket: `dataproc-bucket-<student_id>`
   - File: `sales_data_<student_id>.csv` with at least 3 rows and columns: `id,sale_date,amount,region`

3. **Run a PySpark job on Dataproc**
   - The job should read the CSV from the bucket, calculate total sales per region, and write the result to a new file: `output_<student_id>.csv` in the same bucket.

4. **Verify output**
   - Ensure `output_<student_id>.csv` exists in the bucket and contains the total sales per region.

---

## Naming Convention
- All resources must include the student ID as shown above.
- The evaluator will use the student ID input to check for the correct resources.

---

## Verification
- The evaluator workflow will check for the existence and configuration of your cluster, bucket, input/output files, and output data.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation, delete the Dataproc cluster and the Cloud Storage bucket.

---

**See `solution_guide.md` for a full, step-by-step walkthrough.**

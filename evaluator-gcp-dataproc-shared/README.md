# GCP Dataproc Shared Cluster Evaluator – Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All students will use a shared Dataproc cluster and shared Cloud Storage bucket (see `pre_setup.md`).


### Tasks
1. **Create a Cloud Storage bucket and upload your input file**
   - Create a bucket named `dataproc-shared-bucket` (if not already created by your instructor; otherwise, use the shared bucket).
   - Create a CSV file named `sales_data_<student_id>.csv` with at least 3 rows and columns: `id,sale_date,amount,region`
   - Example data:
     ```csv
     id,sale_date,amount,region
     1,2023-01-01,100.5,West
     2,2023-01-02,200.0,East
     3,2023-01-03,150.75,North
     ```
   - Upload this file to the shared bucket: `gs://dataproc-shared-bucket/`

2. **Write and submit a PySpark job to the shared Dataproc cluster**
   - The job must:
     - Read your own input file: `gs://dataproc-shared-bucket/sales_data_<student_id>.csv`
     - Calculate total sales per region
     - Write the result to: `gs://dataproc-shared-bucket/output_<student_id>.csv`

3. **Verify output**
   - Ensure `output_<student_id>.csv` exists in the shared bucket and contains the total sales per region.

---

## Naming Convention
- Input file: `sales_data_<student_id>.csv` in the shared bucket
- Output file: `output_<student_id>.csv` in the shared bucket
- The evaluator will use the student ID input to check for the correct files.

---

## Verification
- The evaluator workflow will check for the existence and content of your input and output files in the shared bucket.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete your resources after evaluation, remove your input and output files from the shared bucket. The shared cluster and bucket are managed by the instructor.

---

**See `solution_guide.md` for a full, step-by-step walkthrough.**

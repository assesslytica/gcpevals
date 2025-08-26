

# GCP Bigtable Evaluator – Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All resources must be named using the convention: `<resource>-<student_id>` (replace `<student_id>` with your actual student ID).

### Tasks
1. **Create a Bigtable instance**
	- Name/ID: `bigtable-instance-<student_id>`
	- Region: `asia-south1` (unless otherwise instructed)
	- Type: Development (sufficient for this test)

2. **Create a table and schema**
	- Table: `sales_table_<student_id>`
	- Column family: `cf1`

3. **Load sample data**
	- Insert at least 3 rows into `sales_table_<student_id>`
	- Each row must have columns in `cf1`:
	  - `date` (e.g., `2023-01-01`)
	  - `amount` (e.g., `100.5`)
	  - `region` (e.g., `West`)

4. **Grant access to evaluator**
	- Ensure the evaluator service account (provided by your instructor or workflow) has **Bigtable Reader** access to your instance.

---

## Naming Convention
- All resources must include the student ID as shown above.
- The evaluator will use the student ID input to check for the correct resources.

---

## Verification
- The evaluator workflow will check for the existence and configuration of your instance, table, column family, and data.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation, delete the Bigtable instance (which will remove the table and data as well).

---

**See `solution_guide.md` for a full, step-by-step walkthrough.**

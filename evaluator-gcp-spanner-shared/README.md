# GCP Spanner Shared Instance Evaluator – Data Engineering Tasks

## Student Task

You are required to complete the following tasks in your assigned GCP project. All students will use a shared Spanner instance and database (see `pre_setup.md`).

### Tasks

1. **Create your own table in the shared Spanner database**

   - Table name: `sales_data_<student_id>`
   - Columns: `id` (INT64, PRIMARY KEY), `sale_date` (DATE), `amount` (FLOAT64), `region` (STRING(50))
2. **Insert sample data**

   - Insert at least 3 rows into your table with realistic values.
3. **Write and run a query**

   - Write a SQL query to calculate total sales per region from your table.
   - Save the query and its output (screenshot or result file).
4. **Verify your work**

   - Ensure your table exists, has the correct schema, contains at least 3 rows, and your query returns the expected result.

---

## Naming Convention

- Table: `sales_data_<student_id>` in the shared database
- The evaluator will use the student ID input to check for the correct table.

---

## Verification

- The evaluator workflow will check for the existence and content of your table in the shared Spanner database.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)

To delete your resources after evaluation, remove your table from the shared database. The shared instance and database are managed by the instructor.

---


---

## How to Run the Evaluator

- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

### Shared Resource Summary
- Spanner instance: `spanner-shared-instance`
- Spanner database: `spanner_shared_db`

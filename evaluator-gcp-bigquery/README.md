# GCP BigQuery Evaluator – Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All resources must be named using the convention: `<resource>_<student_id>` (replace `<student_id>` with your actual student ID).


### Tasks
1. **Create a BigQuery dataset**
   - Name: `bq_dataset_<student_id>`
   - Location: `asia-south1` (unless otherwise instructed)

2. **Create a table and schema**
   - Table: `sales_data_<student_id>`
   - Columns:
     - `id` (INT64, PRIMARY KEY)
     - `sale_date` (DATE)
     - `amount` (FLOAT64)
     - `region` (STRING)

3. **Load sample data**
   - Insert at least 3 rows into `sales_data_<student_id>` with realistic values.

4. **Write and run a data engineering query**
   - Write a SQL query that returns the total sales amount per region from your table, e.g.:
     ```sql
     SELECT region, SUM(amount) AS total_sales
     FROM `bq_dataset_<student_id>.sales_data_<student_id>`
     GROUP BY region;
     ```
   - Run this query in the BigQuery Console and verify the output.

---

## Naming Convention
- All resources must include the student ID as shown above.
- The evaluator will use the student ID input to check for the correct resources.

---

## Verification
- The evaluator workflow will check for the existence and configuration of your dataset, table, schema, and data.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation, delete the BigQuery dataset (which will remove the table and data as well).

---

**See `solution_guide.md` for a full, step-by-step walkthrough.**

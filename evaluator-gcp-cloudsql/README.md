
# GCP Cloud SQL Evaluator - Data Engineering Tasks

## Student Task
You are required to complete the following tasks in your assigned GCP project. All resources must be named using the convention: `<resource>-<student_id>` (replace `<student_id>` with your actual student ID).

### Tasks
1. **Create a Cloud SQL instance**
   - Name: `sql-instance-<student_id>`
   - Region: `asia-south1`
   - MySQL 8.0, public IP enabled

2. **Create a database and schema**
   - Database: `studentdb_<student_id>`
   - In this database, create a table named `sales_data_<student_id>` with columns:
     - `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
     - `sale_date` (DATE)
     - `amount` (FLOAT)
     - `region` (VARCHAR(50))

3. **Load sample data**
   - Insert at least 3 rows into `sales_data_<student_id>` with realistic values.


4. **Create a user and grant access**
   - User: `studentuser_<student_id>`
   - Password: (any, must be set)
   - Grant this user SELECT and INSERT privileges on `sales_data_<student_id>`.

---

**Important:**
- When creating your Cloud SQL instance, you must set the root (admin) password to: `X9085565r`.
- This password is required for the evaluator to connect and check your work. If you use a different password, your evaluation will fail.

---

## Naming Convention
- All resources must include the student ID as shown above.
- The evaluator will use the student ID input to check for the correct resources.

---

## Verification
- The evaluator workflow will check for the existence and configuration of all resources, table schema, data, and user privileges.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation, delete the Cloud SQL instance (which will remove the database and user as well).

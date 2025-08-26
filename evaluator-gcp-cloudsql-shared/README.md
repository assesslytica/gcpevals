# Cloud SQL Shared Instance Evaluator: Customer Feedback Analytics

## Case Study: Customer Feedback Analytics with Cloud SQL (Shared Instance)

### Scenario
You are a data engineer for a SaaS company. Customer feedback is collected in a shared Cloud SQL (PostgreSQL) database (`feedback_shared_db`) in a shared instance (`cloudsql-shared-instance`). Your job is to create your own table, insert feedback data, analyze sentiment counts, and save your query output to a Cloud Storage bucket you create.

### Task Overview
1. **Create Table**: In the shared database, create a table named `feedback_{student_id}` with columns:
   - `id` (SERIAL PRIMARY KEY)
   - `customer_id` (VARCHAR)
   - `feedback_text` (TEXT)
   - `sentiment` (VARCHAR, e.g., 'positive', 'neutral', 'negative')
2. **Insert Data**: Insert at least 3 rows of sample feedback with different sentiments.
3. **Query**: Write a SQL query to count feedbacks by sentiment.
4. **Save Output**: Save the output of your query as a CSV file in a Cloud Storage bucket named `cloudsql-feedback-{student_id}`.
5. **Verification**: The evaluator will check:
   - Table existence and schema.
   - Row count (at least 3).
   - Query result correctness.
   - Output file exists in the correct bucket and matches the query result.

### Shared Resources (Instructor Pre-Setup)
- Cloud SQL instance: `cloudsql-shared-instance` (PostgreSQL)
- Database: `feedback_shared_db`
- All students have DDL/DML access to the shared database (no individual instances).

### OIDC Authentication
- All access is via OIDC (no password sharing or service account keys).
- Students connect using IAM authentication.

---

## How to Run the Evaluator
- Trigger the GitHub Actions workflow manually with your `student_id`.
- The evaluator will log results and upload a report for download.
- **Authentication is handled via OIDC (OpenID Connect) using GitHub Actions. You do NOT need to upload or use a service account key.**

---

### Note on Authentication
This evaluator uses OIDC for secure, keyless authentication. As long as your instructor has set up the OIDC provider and granted the correct permissions, you do not need to manage or upload any service account keys. All access is handled automatically by the workflow.

# Solution Guide: Customer Feedback Analytics with Cloud SQL (Shared Instance)

This guide will walk you through the process step by step, with explanations and sample commands. No prior GCP experience is required.

---

## 1. Connect to the Shared Cloud SQL Database
1. Go to the [Cloud SQL Console](https://console.cloud.google.com/sql/instances).
2. Find the instance `cloudsql-shared-instance` and database `feedback_shared_db`.
3. Use the Cloud Shell or `gcloud` to connect using IAM authentication:
   ```bash
   gcloud sql connect cloudsql-shared-instance --user=$(gcloud config get-value account) --database=feedback_shared_db
   ```

---

## 2. Create Your Table
1. In the SQL prompt, run:
   ```sql
   CREATE TABLE feedback_{student_id} (
     id SERIAL PRIMARY KEY,
     customer_id VARCHAR(64),
     feedback_text TEXT,
     sentiment VARCHAR(16)
   );
   ```

---

## 3. Insert Sample Data
1. Insert at least 3 rows with different sentiments:
   ```sql
   INSERT INTO feedback_{student_id} (customer_id, feedback_text, sentiment) VALUES
     ('cust1', 'Great product!', 'positive'),
     ('cust2', 'Could be better.', 'neutral'),
     ('cust3', 'Very disappointed', 'negative');
   ```

---

## 4. Write and Run Your Query
1. Count feedbacks by sentiment:
   ```sql
   SELECT sentiment, COUNT(*) AS count FROM feedback_{student_id} GROUP BY sentiment;
   ```
2. Save the output as a CSV file (see next step).

---

## 5. Save Query Output to Cloud Storage
1. Create a bucket named `cloudsql-feedback-{student_id}`:
   ```bash
   gsutil mb gs://cloudsql-feedback-{student_id}
   ```
2. Export your query result to CSV (from Cloud Shell):
   ```bash
   gcloud sql export csv cloudsql-shared-instance gs://cloudsql-feedback-{student_id}/sentiment_counts_{student_id}.csv \
     --database=feedback_shared_db \
     --query="SELECT sentiment, COUNT(*) AS count FROM feedback_{student_id} GROUP BY sentiment;"
   ```

---

## 6. Verify Your Results
- Ensure your table exists and has at least 3 rows.
- Ensure your output CSV exists in the correct bucket and matches your query result.

---

## 7. Clean Up (Optional)
- Drop your table and delete your bucket if instructed.

---

## Tips
- Use OIDC/IAM authentication for all access (no password or key needed).
- If you get permission errors, check with your instructor that your account is added and OIDC is set up.
- Ask for help if you get stuck—this is a learning exercise!

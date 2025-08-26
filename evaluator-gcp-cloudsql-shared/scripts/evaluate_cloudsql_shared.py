import os
import sys
import logging
import psycopg2
from google.cloud import storage

# Logging setup
LOG_FILE = "test_report.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)

PASS = 0
FAIL = 0

def log_result(success, message):
    global PASS, FAIL
    if success:
        logging.info(f"PASS: {message}")
        PASS += 1
    else:
        logging.error(f"FAIL: {message}")
        FAIL += 1

def main():
    # Environment variables (set by workflow)
    DB_HOST = os.environ.get("CLOUDSQL_HOST")
    DB_PORT = os.environ.get("CLOUDSQL_PORT", "5432")
    DB_USER = os.environ.get("CLOUDSQL_USER")
    DB_PASS = os.environ.get("CLOUDSQL_PASSWORD")
    DB_NAME = os.environ.get("CLOUDSQL_DBNAME")
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    STUDENT_ID = os.environ.get("STUDENT_ID")

    # Task 1: Connect to Cloud SQL (Postgres)
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME
        )
        log_result(True, "Connected to Cloud SQL instance.")
    except Exception as e:
        log_result(False, f"Could not connect to Cloud SQL: {e}")
        sys.exit(1)

    # Task 2: Check for table and schema
    table_name = f"student_{STUDENT_ID}_records"
    expected_columns = ["id", "name", "score"]
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
            columns = [row[0] for row in cur.fetchall()]
            if all(col in columns for col in expected_columns):
                log_result(True, f"Table {table_name} exists with correct schema.")
            else:
                log_result(False, f"Table {table_name} schema incorrect. Columns found: {columns}")
    except Exception as e:
        log_result(False, f"Error checking table schema: {e}")

    # Task 3: Check row count >= 3
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            if count >= 3:
                log_result(True, f"Table {table_name} has at least 3 rows.")
            else:
                log_result(False, f"Table {table_name} has less than 3 rows ({count}).")
    except Exception as e:
        log_result(False, f"Error checking row count: {e}")

    # Task 4: Check query result and output file in bucket
    output_file = f"{STUDENT_ID}_query_output.csv"
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name} WHERE score >= 80")
            rows = cur.fetchall()
            if rows:
                log_result(True, f"Query for score >= 80 returned {len(rows)} rows.")
            else:
                log_result(False, "Query for score >= 80 returned no rows.")
            # Save to CSV
            import csv
            with open(output_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(expected_columns)
                for row in rows:
                    writer.writerow(row)
    except Exception as e:
        log_result(False, f"Error running query or saving CSV: {e}")

    # Task 5: Check file uploaded to bucket
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(output_file)
        blob.upload_from_filename(output_file)
        log_result(True, f"Uploaded {output_file} to bucket {BUCKET_NAME}.")
    except Exception as e:
        log_result(False, f"Error uploading file to bucket: {e}")

    # Summary
    logging.info(f"TOTAL PASS: {PASS}")
    logging.info(f"TOTAL FAIL: {FAIL}")
    if FAIL == 0:
        logging.info("All checks passed!")
    else:
        logging.info("Some checks failed. See above for details.")

if __name__ == "__main__":
    main()

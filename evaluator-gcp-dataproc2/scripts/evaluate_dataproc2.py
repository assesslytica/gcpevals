import sys
import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")


def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)


def check_bigquery_table(student_id):
    global PASS, FAIL
    client = bigquery.Client()
    dataset = 'retail_shared'
    table = f'analytics_results.sales_summary_{student_id}'
    table_ref = f"{client.project}.{dataset}.{table}"
    try:
        t = client.get_table(table_ref)
        log(f"PASS: BigQuery table {table_ref} exists.")
        PASS += 1
        return t
    except Exception as e:
        log(f"FAIL: BigQuery table {table_ref} not found or error: {e}")
        FAIL += 1
        return None


def check_bigquery_schema(table):
    global PASS, FAIL
    expected = {'store_id', 'sale_date', 'total_sales'}
    actual = set([field.name for field in table.schema])
    if expected.issubset(actual):
        log(f"PASS: BigQuery table schema is correct: {actual}")
        PASS += 1
        return True
    else:
        log(f"FAIL: BigQuery table schema incorrect: {actual}")
        FAIL += 1
        return False


def check_bigquery_data(table):
    global PASS, FAIL
    client = bigquery.Client()
    table_ref = table.reference
    query = f"SELECT COUNT(*) as row_count FROM `{table_ref}`"
    result = list(client.query(query))
    row_count = result[0].row_count if result else 0
    if row_count > 0:
        log(f"PASS: BigQuery table {table_ref} has {row_count} rows.")
        PASS += 1
        return True
    else:
        log(f"FAIL: BigQuery table {table_ref} is empty.")
        FAIL += 1
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_dataproc2.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    table = check_bigquery_table(student_id)
    if table:
        check_bigquery_schema(table)
        check_bigquery_data(table)
    total = PASS + FAIL
    log(f"TOTAL_SCORE: {PASS}/{total}")
    if FAIL == 0:
        log("OVERALL: PASS")
    else:
        log("OVERALL: FAIL")
    print("\n--- test_report.log contents ---")
    with open(LOG_PATH, 'r') as f:
        print(f.read())
    print("\nYou can download test_report.log from the workflow artifacts.")


if __name__ == "__main__":
    main()

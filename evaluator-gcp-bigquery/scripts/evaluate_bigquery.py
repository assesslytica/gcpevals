import sys
import os
from google.cloud import bigquery

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_dataset(student_id, project):
    global PASS, FAIL
    dataset_id = f"bq_dataset_{student_id}"
    full_dataset_id = f"{project}.{dataset_id}"
    client = bigquery.Client(project=project)
    try:
        dataset = client.get_dataset(full_dataset_id)
        log(f"PASS: Dataset {full_dataset_id} exists")
        PASS += 1
        return dataset
    except Exception as e:
        log(f"FAIL: Dataset {full_dataset_id} not found or error: {e}")
        FAIL += 1
        return None

def check_table(student_id, project, dataset):
    global PASS, FAIL
    table_id = f"sales_data_{student_id}"
    full_table_id = f"{dataset.project}.{dataset.dataset_id}.{table_id}"
    client = bigquery.Client(project=project)
    try:
        table = client.get_table(full_table_id)
        log(f"PASS: Table {full_table_id} exists")
        PASS += 1
        return table
    except Exception as e:
        log(f"FAIL: Table {full_table_id} not found or error: {e}")
        FAIL += 1
        return None

def check_schema(table):
    global PASS, FAIL
    expected = [
        ("id", "INTEGER"),
        ("sale_date", "DATE"),
        ("amount", "FLOAT"),
        ("region", "STRING")
    ]
    actual = [(f.name, f.field_type) for f in table.schema]
    for name, typ in expected:
        if (name, typ) in actual:
            log(f"PASS: Column {name} type {typ}")
            PASS += 1
        else:
            log(f"FAIL: Column {name} type {typ} not found in table schema")
            FAIL += 1

def check_rows(table, project):
    global PASS, FAIL
    client = bigquery.Client(project=project)
    query = f"SELECT COUNT(*) as cnt FROM `{table.project}.{table.dataset_id}.{table.table_id}`"
    try:
        result = client.query(query).result()
        count = list(result)[0]["cnt"]
        if count >= 3:
            log(f"PASS: Table has at least 3 rows (found {count})")
            PASS += 1
        else:
            log(f"FAIL: Table has less than 3 rows (found {count})")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error counting rows: {e}")
        FAIL += 1


def check_total_sales_query(student_id, project):
    global PASS, FAIL
    client = bigquery.Client(project=project)
    query = f"""
        SELECT region, SUM(amount) AS total_sales
        FROM `bq_dataset_{student_id}.sales_data_{student_id}`
        GROUP BY region
    """
    try:
        result = list(client.query(query).result())
        if result and all('region' in row and 'total_sales' in row for row in result):
            log(f"PASS: Data engineering query ran successfully and returned {len(result)} rows.")
            PASS += 1
        else:
            log(f"FAIL: Data engineering query did not return expected results.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error running data engineering query: {e}")
        FAIL += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_bigquery.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    dataset = check_dataset(student_id, project)
    if dataset:
        table = check_table(student_id, project, dataset)
        if table:
            check_schema(table)
            check_rows(table, project)
            check_total_sales_query(student_id, project)
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

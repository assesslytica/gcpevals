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

def check_table(student_id, project):
    global PASS, FAIL
    dataset_id = "dataflow_shared"
    table_id = f"dataflow_output_{student_id}"
    full_table_id = f"{project}.{dataset_id}.{table_id}"
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
        ("sale_date", "STRING"),
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_dataflow.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    table = check_table(student_id, project)
    if table:
        check_schema(table)
        check_rows(table, project)
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

import sys
import os
from google.cloud import spanner

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

INSTANCE_ID = "spanner-shared-instance"
DATABASE_ID = "spanner_shared_db"

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_table(student_id, project):
    global PASS, FAIL
    table_name = f"sales_data_{student_id}"
    client = spanner.Client(project=project)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)
    # Check table existence and schema
    try:
        ddl = database.ddl()
        found = False
        for stmt in ddl:
            if stmt.strip().startswith(f"CREATE TABLE {table_name} "):
                found = True
                if all(col in stmt for col in ["id INT64", "sale_date DATE", "amount FLOAT64", "region STRING(50)"]):
                    log(f"PASS: Table {table_name} exists with correct schema")
                    PASS += 1
                else:
                    log(f"FAIL: Table {table_name} schema is incorrect")
                    FAIL += 1
                break
        if not found:
            log(f"FAIL: Table {table_name} not found in database {DATABASE_ID}")
            FAIL += 1
            return None
    except Exception as e:
        log(f"FAIL: Error checking table DDL: {e}")
        FAIL += 1
        return None
    return database

def check_rows(student_id, database):
    global PASS, FAIL
    table_name = f"sales_data_{student_id}"
    try:
        with database.snapshot() as snapshot:
            results = list(snapshot.execute_sql(f"SELECT * FROM {table_name}"))
            if len(results) >= 3:
                log(f"PASS: Table {table_name} has at least 3 rows (found {len(results)})")
                PASS += 1
            else:
                log(f"FAIL: Table {table_name} has less than 3 rows (found {len(results)})")
                FAIL += 1
    except Exception as e:
        log(f"FAIL: Error reading rows from {table_name}: {e}")
        FAIL += 1

def check_query(student_id, database):
    global PASS, FAIL
    table_name = f"sales_data_{student_id}"
    try:
        with database.snapshot() as snapshot:
            results = list(snapshot.execute_sql(f"SELECT region, SUM(amount) AS total_sales FROM {table_name} GROUP BY region"))
            if results and all(len(row) == 2 for row in results):
                log(f"PASS: Query for total sales per region ran successfully and returned {len(results)} rows.")
                PASS += 1
            else:
                log(f"FAIL: Query did not return expected results.")
                FAIL += 1
    except Exception as e:
        log(f"FAIL: Error running query: {e}")
        FAIL += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_spanner_shared.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    database = check_table(student_id, project)
    if database:
        check_rows(student_id, database)
        check_query(student_id, database)
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

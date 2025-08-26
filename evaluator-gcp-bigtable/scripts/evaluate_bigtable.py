
import sys
import os
from google.cloud import bigtable
from google.cloud.bigtable import row_filters

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_instance(student_id, project):
    global PASS, FAIL
    instance_id = f"bigtable-instance-{student_id}"
    try:
        client = bigtable.Client(project=project, admin=True)
        instance = client.instance(instance_id)
        if not instance.exists():
            log(f"FAIL: Instance {instance_id} not found.")
            FAIL += 1
            return None
        log(f"PASS: Instance {instance_id} exists")
        PASS += 1
        return instance
    except Exception as e:
        log(f"FAIL: Error connecting to instance {instance_id}: {e}")
        FAIL += 1
        return None

def check_table(student_id, instance):
    global PASS, FAIL
    table_id = f"sales_table_{student_id}"
    try:
        table = instance.table(table_id)
        if not table.exists():
            log(f"FAIL: Table {table_id} not found.")
            FAIL += 1
            return None
        log(f"PASS: Table {table_id} exists")
        PASS += 1
        return table
    except Exception as e:
        log(f"FAIL: Error connecting to table {table_id}: {e}")
        FAIL += 1
        return None

def check_column_family(table):
    global PASS, FAIL
    cf_id = "cf1"
    try:
        cfamilies = table.list_column_families()
        if cf_id not in cfamilies:
            log(f"FAIL: Column family {cf_id} not found.")
            FAIL += 1
            return False
        log(f"PASS: Column family {cf_id} exists")
        PASS += 1
        return True
    except Exception as e:
        log(f"FAIL: Error checking column family {cf_id}: {e}")
        FAIL += 1
        return False

def check_rows(table):
    global PASS, FAIL
    try:
        row_count = 0
        sample_rows = []
        partial_rows = table.read_rows(filter_=row_filters.CellsColumnLimitFilter(1))
        for row in partial_rows:
            row_count += 1
            if row_count <= 3:
                sample_rows.append(row)
        if row_count >= 3:
            log(f"PASS: Table has at least 3 rows (found {row_count})")
            PASS += 1
        else:
            log(f"FAIL: Table has less than 3 rows (found {row_count})")
            FAIL += 1
        # Check sample data
        for idx, row in enumerate(sample_rows, 1):
            try:
                cf = row.cells["cf1"]
                has_date = any(col.qualifier.decode() == 'date' for col in cf)
                has_amount = any(col.qualifier.decode() == 'amount' for col in cf)
                has_region = any(col.qualifier.decode() == 'region' for col in cf)
                if has_date and has_amount and has_region:
                    log(f"PASS: Sample row {idx} has date, amount, region")
                    PASS += 1
                else:
                    log(f"FAIL: Sample row {idx} missing columns in row {row.row_key.decode()}")
                    FAIL += 1
            except Exception as e:
                log(f"FAIL: Error checking sample row {idx}: {e}")
                FAIL += 1
    except Exception as e:
        log(f"FAIL: Error scanning rows: {e}")
        FAIL += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_bigtable.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    instance = check_instance(student_id, project)
    if instance:
        table = check_table(student_id, instance)
        if table:
            if check_column_family(table):
                check_rows(table)
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

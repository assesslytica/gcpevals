import sys
import os
from google.cloud import storage
import csv
import tempfile

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

SHARED_BUCKET = "dataproc-shared-bucket"


def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)


def check_input_file(student_id, project):
    global PASS, FAIL
    input_file = f"sales_data_{student_id}.csv"
    storage_client = storage.Client(project=project)
    try:
        bucket = storage_client.get_bucket(SHARED_BUCKET)
        log(f"PASS: Shared bucket {SHARED_BUCKET} exists")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Shared bucket {SHARED_BUCKET} not found or error: {e}")
        FAIL += 1
        return None, None
    # Check input file
    blob = storage.Blob(input_file, bucket)
    if blob.exists(storage_client):
        log(f"PASS: Input file {input_file} exists in shared bucket")
        PASS += 1
        # Check input file content (at least 3 rows, correct columns)
        try:
            content = blob.download_as_text()
            reader = csv.DictReader(content.splitlines())
            rows = list(reader)
            if reader.fieldnames == ['id', 'sale_date', 'amount', 'region']:
                log(f"PASS: Input file has correct columns")
                PASS += 1
            else:
                log(f"FAIL: Input file columns are incorrect: {reader.fieldnames}")
                FAIL += 1
            if len(rows) >= 3:
                log(f"PASS: Input file has at least 3 rows (found {len(rows)})")
                PASS += 1
            else:
                log(f"FAIL: Input file has less than 3 rows (found {len(rows)})")
                FAIL += 1
        except Exception as e:
            log(f"FAIL: Error reading input file: {e}")
            FAIL += 1
    else:
        log(f"FAIL: Input file {input_file} not found in shared bucket")
        FAIL += 1
    return bucket, input_file

def check_output_file(student_id, bucket):
    global PASS, FAIL
    output_blob = None
    for blob in bucket.list_blobs(prefix=f"output_{student_id}"):
        if blob.name.endswith('.csv'):
            output_blob = blob
            break
    if output_blob:
        log(f"PASS: Output file {output_blob.name} exists in shared bucket")
        PASS += 1
    else:
        log(f"FAIL: Output file output_{student_id}.csv not found in shared bucket")
        FAIL += 1
    return output_blob

def check_output_data(output_blob):
    global PASS, FAIL
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            output_blob.download_to_filename(tmp.name)
            tmp.seek(0)
            reader = csv.DictReader(tmp)
            regions = set()
            for row in reader:
                if 'region' in row and 'total_sales' in row:
                    regions.add(row['region'])
            if len(regions) >= 1:
                log(f"PASS: Output file contains total sales per region for {len(regions)} region(s)")
                PASS += 1
            else:
                log(f"FAIL: Output file does not contain expected columns or data")
                FAIL += 1
    except Exception as e:
        log(f"FAIL: Error reading output file: {e}")
        FAIL += 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_dataproc_shared.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    bucket, input_file = check_input_file(student_id, project)
    output_blob = None
    if bucket:
        output_blob = check_output_file(student_id, bucket)
    if output_blob:
        check_output_data(output_blob)
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

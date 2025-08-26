import sys
import os
from google.cloud import dataproc_v1
from google.cloud import storage
import csv
import tempfile

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_cluster(student_id, project, region):
    global PASS, FAIL
    cluster_name = f"dataproc-cluster-{student_id}"
    client = dataproc_v1.ClusterControllerClient(client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"})
    try:
        cluster = client.get_cluster(project_id=project, region=region, cluster_name=cluster_name)
        log(f"PASS: Cluster {cluster_name} exists in {region}")
        PASS += 1
        return cluster
    except Exception as e:
        log(f"FAIL: Cluster {cluster_name} not found or error: {e}")
        FAIL += 1
        return None

def check_bucket_and_files(student_id, project):
    global PASS, FAIL
    bucket_name = f"dataproc-bucket-{student_id}"
    input_file = f"sales_data_{student_id}.csv"
    output_prefix = f"output_{student_id}.csv"
    storage_client = storage.Client(project=project)
    try:
        bucket = storage_client.get_bucket(bucket_name)
        log(f"PASS: Bucket {bucket_name} exists")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Bucket {bucket_name} not found or error: {e}")
        FAIL += 1
        return None, None, None
    # Check input file
    if storage.Blob(input_file, bucket).exists(storage_client):
        log(f"PASS: Input file {input_file} exists in bucket")
        PASS += 1
    else:
        log(f"FAIL: Input file {input_file} not found in bucket")
        FAIL += 1
    # Check output file (may be in a subfolder)
    output_blob = None
    for blob in bucket.list_blobs(prefix=f"output_{student_id}"):
        if blob.name.endswith('.csv'):
            output_blob = blob
            break
    if output_blob:
        log(f"PASS: Output file {output_blob.name} exists in bucket")
        PASS += 1
    else:
        log(f"FAIL: Output file output_{student_id}.csv not found in bucket")
        FAIL += 1
    return bucket, input_file, output_blob

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
        print("Usage: python evaluate_dataproc.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    region = 'asia-south1'
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    cluster = check_cluster(student_id, project, region)
    bucket, input_file, output_blob = check_bucket_and_files(student_id, project)
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

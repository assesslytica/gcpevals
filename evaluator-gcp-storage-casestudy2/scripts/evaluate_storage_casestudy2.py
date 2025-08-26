
import sys
import os
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden

PASS = 0
FAIL = 0
LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def main():
    global PASS, FAIL
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    STUDENT_ID = os.environ.get("STUDENT_ID")
    COLLAB_EMAIL = os.environ.get("COLLAB_EMAIL")
    DOWNLOAD_STUDENT_ID = os.environ.get("DOWNLOAD_STUDENT_ID")
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    folder = f"{STUDENT_ID}/"

    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {STUDENT_ID}\n")
        f.write("----------------------------------------\n")

    # Task 1: Check folder and CSV upload
    try:
        blobs = list(storage_client.list_blobs(BUCKET_NAME, prefix=folder))
        csv_blobs = [b for b in blobs if b.name.endswith('.csv')]
        if csv_blobs:
            log(f"PASS: CSV file(s) found in {folder}: {[b.name for b in csv_blobs]}")
            PASS += 1
        else:
            log(f"FAIL: No CSV files found in {folder}")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error listing CSVs: {e}")
        FAIL += 1

    # Task 2: Check retention policy (bucket-level, as folder-level not supported)
    try:
        policy = bucket.retention_policy_locked
        if bucket.retention_period and bucket.retention_period >= 604800:  # 7 days in seconds
            log(f"PASS: Retention policy set to {bucket.retention_period} seconds.")
            PASS += 1
        else:
            log("FAIL: Retention policy not set to 7 days or more.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error checking retention policy: {e}")
        FAIL += 1

    # Task 3: Check collaborator has access
    try:
        all_ok = True
        for blob in csv_blobs:
            acl = bucket.blob(blob.name).acl
            acl.reload()
            found = any(entry['entity'] == f'user-{COLLAB_EMAIL}' and entry['role'] == 'READER' for entry in acl)
            if not found:
                all_ok = False
                log(f"FAIL: Collaborator {COLLAB_EMAIL} does not have READER on {blob.name}")
                FAIL += 1
        if all_ok and csv_blobs:
            log(f"PASS: Collaborator {COLLAB_EMAIL} has READER access to all CSVs.")
            PASS += 1
    except Exception as e:
        log(f"FAIL: Error checking collaborator ACLs: {e}")
        FAIL += 1

    # Task 4: Download another student's file and log size
    try:
        download_blob = None
        download_prefix = f"{DOWNLOAD_STUDENT_ID}/"
        for blob in storage_client.list_blobs(BUCKET_NAME, prefix=download_prefix):
            if blob.name.endswith('.csv'):
                download_blob = blob
                break
        if download_blob:
            download_blob.download_to_filename("downloaded_file.csv")
            log(f"PASS: Downloaded {download_blob.name}, size: {download_blob.size} bytes")
            PASS += 1
        else:
            log(f"FAIL: No CSV file found in {download_prefix}")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error downloading file: {e}")
        FAIL += 1

    # Task 5: Delete a test file and verify
    try:
        test_blob_name = f"{folder}testfile.csv"
        test_blob = bucket.blob(test_blob_name)
        if test_blob.exists():
            test_blob.delete()
            if not test_blob.exists():
                log(f"PASS: Deleted {test_blob_name} and verified removal.")
                PASS += 1
            else:
                log(f"FAIL: Failed to delete {test_blob_name}.")
                FAIL += 1
        else:
            log(f"PASS: Test file {test_blob_name} does not exist (nothing to delete).")
            PASS += 1
    except Exception as e:
        log(f"FAIL: Error deleting test file: {e}")
        FAIL += 1

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


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
    TEAM_EMAIL = os.environ.get("TEAM_EMAIL")
    folder = f"{STUDENT_ID}/"
    archive_folder = f"{STUDENT_ID}/archive/"
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {STUDENT_ID}\n")
        f.write("----------------------------------------\n")

    # Task 1: Check at least 3 image files uploaded
    try:
        blobs = list(storage_client.list_blobs(BUCKET_NAME, prefix=folder))
        image_blobs = [b for b in blobs if b.name.endswith(('.jpg', '.jpeg', '.png')) and '/' in b.name[len(folder):]]
        if len(image_blobs) >= 3:
            log(f"PASS: Found {len(image_blobs)} image files in {folder}.")
            PASS += 1
        else:
            log(f"FAIL: Less than 3 image files found in {folder}.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error listing images: {e}")
        FAIL += 1

    # Task 2: Check object-level permissions for team
    try:
        all_ok = True
        for blob in image_blobs:
            acl = bucket.blob(blob.name).acl
            acl.reload()
            found = any(entry['entity'] == f'group-{TEAM_EMAIL}' and entry['role'] == 'READER' for entry in acl)
            if not found:
                all_ok = False
                log(f"FAIL: Team group {TEAM_EMAIL} does not have READER on {blob.name}")
                FAIL += 1
        if all_ok and image_blobs:
            log(f"PASS: All images have READER access for {TEAM_EMAIL}.")
            PASS += 1
    except Exception as e:
        log(f"FAIL: Error checking ACLs: {e}")
        FAIL += 1

    # Task 3: List files and log names/sizes
    try:
        for blob in image_blobs:
            log(f"PASS: File: {blob.name}, Size: {blob.size} bytes")
            PASS += 1
    except Exception as e:
        log(f"FAIL: Error logging file details: {e}")
        FAIL += 1

    # Task 4: Check file moved to archive
    try:
        archive_blobs = list(storage_client.list_blobs(BUCKET_NAME, prefix=archive_folder))
        if archive_blobs:
            log(f"PASS: Found file(s) in archive: {[b.name for b in archive_blobs]}")
            PASS += 1
        else:
            log(f"FAIL: No files found in archive folder {archive_folder}")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error checking archive folder: {e}")
        FAIL += 1

    # Task 5: Generate and test signed URL
    try:
        if image_blobs:
            from datetime import timedelta
            url = bucket.blob(image_blobs[0].name).generate_signed_url(expiration=timedelta(minutes=10), version="v4")
            import requests
            resp = requests.get(url)
            if resp.status_code == 200:
                log(f"PASS: Signed URL works for {image_blobs[0].name}: {url}")
                PASS += 1
            else:
                log(f"FAIL: Signed URL failed for {image_blobs[0].name}: HTTP {resp.status_code}")
                FAIL += 1
        else:
            log("FAIL: No image files to generate signed URL.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error generating/testing signed URL: {e}")
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

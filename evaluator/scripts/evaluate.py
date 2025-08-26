import sys
import os
from google.cloud import storage, pubsub_v1

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_bucket(student_id):
    global PASS, FAIL
    bucket_name = f"eval-{student_id}"
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project:
        log("FAIL: GOOGLE_CLOUD_PROJECT env var not set")
        FAIL += 1
        return
    client = storage.Client(project=project)
    try:
        bucket = client.get_bucket(bucket_name)
        if bucket.location.lower() != 'asia-south1':
            log(f"FAIL: Bucket {bucket_name} not in asia-south1")
            FAIL += 1
            return
        if not bucket.versioning_enabled:
            log(f"FAIL: Bucket {bucket_name} does not have versioning enabled")
            FAIL += 1
            return
        ubla = bucket.iam_configuration.uniform_bucket_level_access
        if not ubla.enabled:
            log(f"FAIL: Bucket {bucket_name} does not have UBLA enabled")
            FAIL += 1
            return
        log(f"PASS: Bucket {bucket_name} meets all requirements")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Bucket {bucket_name} not found or error: {e}")
        FAIL += 1

def check_pubsub_topic(student_id):
    global PASS, FAIL
    topic_name = f"eval-topic-{student_id}"
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project:
        log("FAIL: GOOGLE_CLOUD_PROJECT env var not set")
        FAIL += 1
        return
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    try:
        topic = publisher.get_topic(request={"topic": topic_path})
        log(f"PASS: Pub/Sub topic {topic_name} exists")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Pub/Sub topic {topic_name} not found or error: {e}")
        FAIL += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    # Create/overwrite the log file and write a header
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    check_bucket(student_id)
    check_pubsub_topic(student_id)
    total = PASS + FAIL
    log(f"TOTAL_SCORE: {PASS}/{total}")
    if FAIL == 0:
        log("OVERALL: PASS")
    else:
        log("OVERALL: FAIL")
    # Print the file contents for workflow logs and hint for download
    print("\n--- test_report.log contents ---")
    with open(LOG_PATH, 'r') as f:
        print(f.read())
    print("\nYou can download test_report.log from the workflow artifacts.")

# If you want to upload the log to a bucket, add code here. For now, this is commented out as requested.
# def upload_log_to_bucket(bucket_name, file_path):
#     client = storage.Client()
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(os.path.basename(file_path))
#     blob.upload_from_filename(file_path)

if __name__ == "__main__":
    main()

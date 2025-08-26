import sys
import os
from google.cloud import storage, pubsub_v1

PASS = 0
FAIL = 0

def log(msg):
    with open('test_report.log', 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_bucket(student_id):
    global PASS, FAIL
    bucket_name = f"eval-{student_id}"
    client = storage.Client()
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
        iam_policy = bucket.get_iam_policy(requested_policy_version=3)
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
    publisher = pubsub_v1.PublisherClient()
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project:
        log("FAIL: GOOGLE_CLOUD_PROJECT env var not set")
        FAIL += 1
        return
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
    if os.path.exists('test_report.log'):
        os.remove('test_report.log')
    check_bucket(student_id)
    check_pubsub_topic(student_id)
    total = PASS + FAIL
    log(f"TOTAL_SCORE: {PASS}/{total}")
    if FAIL == 0:
        log("OVERALL: PASS")
    else:
        log("OVERALL: FAIL")

if __name__ == "__main__":
    main()

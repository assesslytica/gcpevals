import os
import sys
from google.cloud import pubsub_v1
import time

PASS = 0
FAIL = 0
LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def main():
    global PASS, FAIL
    STUDENT_ID = os.environ.get("STUDENT_ID")
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    # Use default project from credentials (OIDC)
    # Get project from publisher client
    try:
        project_number = publisher.transport._host.split("-")[0] if hasattr(publisher.transport, '_host') else None
        # But best is to infer from topic/sub path
        # We'll use the publisher's default project
        topic_id = f"iot-sensor-topic-{STUDENT_ID}"
        sub_id = f"iot-sensor-sub-{STUDENT_ID}"
        # Use publisher's default project
        topic_path = publisher.topic_path(publisher.project, topic_id)
        sub_path = subscriber.subscription_path(publisher.project, sub_id)
        schema_id = f"iot_sensor_schema_{STUDENT_ID}"
        schema_path = f"projects/{publisher.project}/schemas/{schema_id}"
    except Exception as e:
        log(f"FAIL: Could not determine GCP project from credentials: {e}")
        FAIL += 1
        return

    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {STUDENT_ID}\n")
        f.write("----------------------------------------\n")

    # Task 1: Check schema exists
    try:
        schema = publisher.get_schema(request={"name": schema_path})
        log(f"PASS: Schema {schema_id} exists.")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Schema {schema_id} not found or error: {e}")
        FAIL += 1
        schema = None

    # Task 2: Check topic exists and is associated with schema
    try:
        topic = publisher.get_topic(request={"topic": topic_path})
        if topic.schema_settings and topic.schema_settings.schema == schema_path:
            log(f"PASS: Topic {topic_id} is associated with schema {schema_id}.")
            PASS += 1
        else:
            log(f"FAIL: Topic {topic_id} is not associated with schema {schema_id}.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Topic {topic_id} not found or error: {e}")
        FAIL += 1

    # Task 3: Check at least 3 valid messages published
    try:
        # Pull messages from subscription
        response = subscriber.pull(request={"subscription": sub_path, "max_messages": 10, "timeout": 10})
        valid_count = 0
        for msg in response.received_messages:
            try:
                data = msg.message.data.decode()
                if all(field in data for field in ["device_id", "timestamp", "temperature", "humidity"]):
                    valid_count += 1
            except Exception:
                continue
        if valid_count >= 3:
            log(f"PASS: At least 3 valid messages found in subscription.")
            PASS += 1
        else:
            log(f"FAIL: Less than 3 valid messages found in subscription.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error pulling messages: {e}")
        FAIL += 1

    # Task 4: Check invalid message was rejected (manual log check)
    # This must be logged by student in test_report.log, so just check for a log entry
    try:
        with open(LOG_PATH, 'r') as f:
            lines = f.readlines()
        found = any("invalid" in line.lower() and "reject" in line.lower() for line in lines)
        if found:
            log(f"PASS: Invalid message rejection was logged.")
            PASS += 1
        else:
            log(f"FAIL: No log entry found for invalid message rejection.")
            FAIL += 1
    except Exception as e:
        log(f"FAIL: Error checking log for invalid message: {e}")
        FAIL += 1

    # Task 5: Check subscription exists and can pull messages
    try:
        sub = subscriber.get_subscription(request={"subscription": sub_path})
        log(f"PASS: Subscription {sub_id} exists.")
        PASS += 1
    except Exception as e:
        log(f"FAIL: Subscription {sub_id} not found or error: {e}")
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

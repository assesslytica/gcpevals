import sys
import os
from google.cloud import sql_v1
from google.cloud.sql.connector import Connector

PASS = 0
FAIL = 0

LOG_PATH = os.path.join(os.path.dirname(__file__), "test_report.log")

def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(msg + '\n')
    print(msg)

def check_sql_instance(student_id, project):
    global PASS, FAIL
    instance_name = f"sql-instance-{student_id}"
    client = sql_v1.SqlInstancesServiceClient()
    try:
        instance = client.get(project=project, instance=instance_name)
        ok = True
        if instance.region == 'asia-south1':
            log(f"PASS: SQL instance {instance_name} is in asia-south1")
            PASS += 1
        else:
            log(f"FAIL: SQL instance {instance_name} not in asia-south1")
            FAIL += 1
            ok = False
        if instance.database_version == sql_v1.SqlDatabaseInstance.DatabaseVersion.MYSQL_8_0:
            log(f"PASS: SQL instance {instance_name} is MySQL 8.0")
            PASS += 1
        else:
            log(f"FAIL: SQL instance {instance_name} is not MySQL 8.0")
            FAIL += 1
            ok = False
        if any(ip.type_ == sql_v1.SqlIpConfig.IpType.PRIMARY for ip in instance.ip_addresses):
            log(f"PASS: SQL instance {instance_name} has a public IP")
            PASS += 1
        else:
            log(f"FAIL: SQL instance {instance_name} does not have a public IP")
            FAIL += 1
            ok = False
        return ok
    except Exception as e:
        log(f"FAIL: SQL instance {instance_name} not found or error: {e}")
        FAIL += 1
        return False

def check_database_and_table(student_id, project, root_user, root_pass):
    global PASS, FAIL
    instance_name = f"sql-instance-{student_id}"
    db_name = f"studentdb_{student_id}"
    table_name = f"sales_data_{student_id}"
    connector = Connector()
    try:
        conn = connector.connect(
            instance_connection_string=f"{project}:asia-south1:{instance_name}",
            driver="mysql",
            user=root_user,
            password=root_pass,
            db=db_name,
        )
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        expected = [
            ('id', 'int', 'NO', 'PRI', None, 'auto_increment'),
            ('sale_date', 'date', 'YES', '', None, ''),
            ('amount', 'float', 'YES', '', None, ''),
            ('region', 'varchar(50)', 'YES', '', None, '')
        ]
        for i, col in enumerate(expected):
            if i >= len(columns):
                log(f"FAIL: Table {table_name} missing column {col[0]}")
                FAIL += 1
            elif not columns[i][0].startswith(col[0]) or not columns[i][1].startswith(col[1]):
                log(f"FAIL: Table {table_name} column {col[0]} type mismatch (expected {col[1]}, got {columns[i][1]})")
                FAIL += 1
            else:
                log(f"PASS: Table {table_name} column {col[0]} type {col[1]}")
                PASS += 1
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        if count >= 3:
            log(f"PASS: Table {table_name} has at least 3 rows")
            PASS += 1
        else:
            log(f"FAIL: Table {table_name} has less than 3 rows")
            FAIL += 1
        cursor.close()
        conn.close()
    except Exception as e:
        log(f"FAIL: Error checking table {table_name} in {db_name}: {e}")
        FAIL += 1

def check_user_privileges(student_id, project, root_user, root_pass):
    global PASS, FAIL
    instance_name = f"sql-instance-{student_id}"
    db_name = f"studentdb_{student_id}"
    table_name = f"sales_data_{student_id}"
    user_name = f"studentuser_{student_id}"
    connector = Connector()
    try:
        conn = connector.connect(
            instance_connection_string=f"{project}:asia-south1:{instance_name}",
            driver="mysql",
            user=root_user,
            password=root_pass,
            db=db_name,
        )
        cursor = conn.cursor()
        cursor.execute(f"SHOW GRANTS FOR '{user_name}'@'%' ")
        grants = cursor.fetchall()
        select_ok = False
        insert_ok = False
        for grant in grants:
            if f"SELECT" in grant[0] and table_name in grant[0]:
                select_ok = True
            if f"INSERT" in grant[0] and table_name in grant[0]:
                insert_ok = True
        if select_ok:
            log(f"PASS: User {user_name} has SELECT on {table_name}")
            PASS += 1
        else:
            log(f"FAIL: User {user_name} does not have SELECT on {table_name}")
            FAIL += 1
        if insert_ok:
            log(f"PASS: User {user_name} has INSERT on {table_name}")
            PASS += 1
        else:
            log(f"FAIL: User {user_name} does not have INSERT on {table_name}")
            FAIL += 1
        cursor.close()
        conn.close()
    except Exception as e:
        log(f"FAIL: Error checking privileges for {user_name}: {e}")
        FAIL += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_cloudsql.py <student_id>")
        sys.exit(1)
    student_id = sys.argv[1]
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    root_user = os.environ.get('CLOUDSQL_ROOT_USER', 'root')
    root_pass = os.environ.get('CLOUDSQL_ROOT_PASS')
    if not project or not root_pass:
        print("GOOGLE_CLOUD_PROJECT or CLOUDSQL_ROOT_PASS env var not set")
        sys.exit(1)
    with open(LOG_PATH, 'w') as f:
        f.write(f"Evaluation Report for student_id: {student_id}\n")
        f.write("----------------------------------------\n")
    if check_sql_instance(student_id, project):
        check_database_and_table(student_id, project, root_user, root_pass)
        check_user_privileges(student_id, project, root_user, root_pass)
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

import os
import logging
from google.cloud import bigquery, spanner
from google.api_core.exceptions import NotFound

logging.basicConfig(level=logging.INFO, filename='etl3_evaluation.log', filemode='w')

STUDENT_ID = os.environ.get('STUDENT_ID')
BQ_DATASET = 'ecom_shared'
BQ_TABLE = 'orders_raw'
SPANNER_INSTANCE = 'ecom-shared-instance'
SPANNER_DATABASE = 'ecom_shared_db'
SPANNER_TABLE = f'order_summary_{STUDENT_ID}'

def check_bigquery_table():
    client = bigquery.Client()
    table_ref = f"{client.project}.{BQ_DATASET}.{BQ_TABLE}"
    try:
        table = client.get_table(table_ref)
        logging.info(f"BigQuery table {table_ref} exists.")
        return table
    except NotFound:
        logging.error(f"BigQuery table {table_ref} not found.")
        return None

def check_spanner_table():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(SPANNER_INSTANCE)
    database = instance.database(SPANNER_DATABASE)
    with database.snapshot() as snapshot:
        results = list(snapshot.execute_sql(
            f"SELECT table_name FROM information_schema.tables WHERE table_name = '{SPANNER_TABLE}'"
        ))
        if results:
            logging.info(f"Spanner table {SPANNER_TABLE} exists.")
            return True
        else:
            logging.error(f"Spanner table {SPANNER_TABLE} does not exist.")
            return False

def check_spanner_schema():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(SPANNER_INSTANCE)
    database = instance.database(SPANNER_DATABASE)
    with database.snapshot() as snapshot:
        results = list(snapshot.execute_sql(
            f"SELECT column_name, spanner_type FROM information_schema.columns WHERE table_name = '{SPANNER_TABLE}'"
        ))
        expected = {('customer_id', 'STRING'), ('order_month', 'STRING'), ('total_value', 'FLOAT64')}
        actual = set((r[0], r[1]) for r in results)
        if expected.issubset(actual):
            logging.info(f"Spanner table {SPANNER_TABLE} schema is correct.")
            return True
        else:
            logging.error(f"Spanner table {SPANNER_TABLE} schema incorrect: {actual}")
            return False

def check_dataflow_job():
    job_id = os.environ.get('DATAFLOW_JOB_ID')
    if not job_id:
        logging.warning("DATAFLOW_JOB_ID not provided. Skipping Dataflow job check.")
        return False
    logging.info(f"Dataflow job {job_id} provided (status check not implemented in this script).")
    return True

def check_spanner_data():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(SPANNER_INSTANCE)
    database = instance.database(SPANNER_DATABASE)
    with database.snapshot() as snapshot:
        results = list(snapshot.execute_sql(
            f"SELECT COUNT(*) FROM {SPANNER_TABLE}"
        ))
        row_count = results[0][0] if results else 0
        if row_count > 0:
            logging.info(f"Spanner table {SPANNER_TABLE} has {row_count} rows.")
            return True
        else:
            logging.error(f"Spanner table {SPANNER_TABLE} is empty.")
            return False

def main():
    ok = True
    if not check_bigquery_table():
        ok = False
    if not check_spanner_table():
        ok = False
    if not check_spanner_schema():
        ok = False
    if not check_dataflow_job():
        ok = False
    if not check_spanner_data():
        ok = False
    if ok:
        logging.info("ETL evaluation PASSED.")
        print("ETL evaluation PASSED.")
    else:
        logging.error("ETL evaluation FAILED. See log for details.")
        print("ETL evaluation FAILED. See log for details.")

if __name__ == "__main__":
    main()

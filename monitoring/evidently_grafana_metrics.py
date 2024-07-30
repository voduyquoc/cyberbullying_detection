import math
import time
import pytz
import logging
import datetime

import pandas as pd
import psycopg
from prefect import flow, task
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import ClassificationPreset

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

create_table_query = """
create table if not exists metrics (
    timestamp timestamp,
    current_accuracy_score float,
    reference_accuracy_score float,
    current_precision_score float,
    reference_precision_score float,
    current_recall_score float,
    reference_recall_score float,
    current_f1_score float,
    reference_f1_score float
);
"""

# Load data and model
current_data = pd.read_csv('./data/current.csv')
current_data = current_data.head(20)
reference_data = pd.read_csv('./data/reference.csv')


col_mapping = ColumnMapping(target='cyberbullying_type', prediction='prediction')

report = Report(metrics=[ClassificationPreset()])


@task
def prep_db(create_table_query):
    """
    Prepare Database
    Ensure that the PostgreSQL database 'evidently' is created and ready for use.

    """
    with psycopg.connect(
        "host=localhost port=5432 user=postgres password=postgres", autocommit=True
    ) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname = 'evidently'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE evidently;")
        with psycopg.connect(
            "host=localhost port=5432 user=postgres password=postgres dbname=evidently",
            autocommit=True,
        ) as conn:
            conn.execute(create_table_query)


@task
def calculate_metrics_postgresql(begin, curr, i):
    """
    Calculate Metrics and Insert into PostgreSQL
    Calculate various metrics using the Evidently library and insert them into the PostgreSQL database.

    Args:
        curr: The PostgreSQL cursor.
        i (int): Index for processing the data in chunks.

    """
    current = current_data.iloc[i * 5 : (i + 1) * 5]
    # current['prediction'] = model.predict(current['processed_text'])

    report.run(current_data=current, 
               reference_data=reference_data, 
               column_mapping=col_mapping
    )
    json_data = report.as_dict()
    
    current_accuracy_score = json_data['metrics'][0]['result']['current']['accuracy']
    reference_accuracy_score = json_data['metrics'][0]['result']['reference']['accuracy']

    current_precision_score = json_data['metrics'][0]['result']['current']['precision']
    reference_precision_score = json_data['metrics'][0]['result']['reference']['precision']

    current_recall_score = json_data['metrics'][0]['result']['current']['recall']
    reference_recall_score = json_data['metrics'][0]['result']['reference']['recall']

    current_f1_score = json_data['metrics'][0]['result']['current']['f1']
    reference_f1_score = json_data['metrics'][0]['result']['reference']['f1']

    curr.execute(
        """
        INSERT INTO metrics (
            timestamp,
            current_accuracy_score,
            reference_accuracy_score,
            current_precision_score,
            reference_precision_score,
            current_recall_score,
            reference_recall_score,
            current_f1_score,
            reference_f1_score
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            begin + datetime.timedelta(i),
            current_accuracy_score,
            reference_accuracy_score,
            current_precision_score,
            reference_precision_score,
            current_recall_score,
            reference_recall_score,
            current_f1_score,
            reference_f1_score,
        ),
    )


@flow
def batch_monitoring():
    """
    Batch Monitoring Flow
    Prefect flow that orchestrates the monitoring process, including metric calculation and database insertion.

    """
    SEND_TIMEOUT = 10
    prep_db(create_table_query)
    ROWS = current_data.shape[0]
    iters = math.ceil(ROWS / 5)
    begin = datetime.datetime.now(pytz.timezone('Europe/Berlin')) - datetime.timedelta(iters)
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect(
        "host=localhost port=5432 dbname=evidently user=postgres password=postgres",
        autocommit=True,
    ) as conn:
        for i in range(iters):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(begin, curr, i)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")


if __name__ == '__main__':
    batch_monitoring()
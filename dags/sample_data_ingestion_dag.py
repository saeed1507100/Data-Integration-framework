from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from app.data_ingestion.data_extraction import extractor
from app.data_ingestion.data_load import loader
import os

default_args = {
    'owner': 'SaeedKhan',
    'retries': 0,
    'retry_delay': timedelta(minutes=2)
}

QUERY = "SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-02'"
FILE_NAME = "covid19_us_states_20201002.csv"
TABLE_NAME = 'covid19_us_states'
REFERENCE_ID = os.environ['SUPABASE_DB_REFERENCE_ID']
PASSWORD = os.environ['SUPABASE_DB_PASSWORD']


def extract_data(ti):
    df = extractor("Google-Cloud").get_data(query=QUERY, file_name=FILE_NAME)
    print(df)


def load_data(ti):
    loader("Supabase").load_data(file_name=FILE_NAME, table=TABLE_NAME, db_reference_id=REFERENCE_ID, db_password=PASSWORD)


with DAG(
        dag_id='sample_data_ingestion_dag_v5',
        default_args=default_args,
        description='Trying out a data ingestion job with airflow (Extract-Load)',
        start_date=datetime(2023, 4, 1, 10),
        schedule_interval='@daily'
) as dag:

    task1 = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data
    )

    task2 = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    task1 >> task2

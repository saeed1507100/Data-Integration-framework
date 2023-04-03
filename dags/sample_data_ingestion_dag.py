from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from app.data_ingestion.data_extraction import extractor
from app.data_ingestion.data_load import loader
import os

default_args = {
    'owner': 'SaeedKhan',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f"Hello world! My Name is {first_name} {last_name}, and I am {age} years old!")


def get_name(ti):
    ti.xcom_push(key='first_name', value='Saeed Anwar')
    ti.xcom_push(key='last_name', value='Khan')


def extract_data(ti):
    df = extractor("Google-Cloud").get_data(
        query="SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-02'"
    )
    print(df)
    ti.xcom_push(key='df', value=df)


def load_data(ti):
    df = ti.xcom_pull(task_ids='extract_data', key='df')
    loader("Supabase").load_data(dataframe=df,
                                 table='covid19_us_states',
                                 db_reference_id=os.environ['SUPABASE_DB_REFERENCE_ID'],
                                 db_password=os.environ['SUPABASE_DB_PASSWORD'])


with DAG(
        dag_id='sample_data_ingestion_dag_v1',
        default_args=default_args,
        description='Trying out a data ingestion job with airflow (Extract-Load)',
        start_date=datetime(2023, 3, 13, 10),
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

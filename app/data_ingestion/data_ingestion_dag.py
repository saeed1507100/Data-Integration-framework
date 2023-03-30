#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
### DAG Tutorial Documentation
This DAG is demonstrating an Extract -> Transform -> Load pipeline
"""
from __future__ import annotations

# [START tutorial]
# [START import_module]
import json
import os
from textwrap import dedent

import pendulum
from data_extraction import extractor
from data_load import loader

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# [END import_module]

# [START instantiate_dag]
with DAG(
        "data_ingestion_dag",
        # [START default_args]
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={"retries": 2},
        # [END default_args]
        description="DAG Data Ingestion",
        schedule=None,
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=["example"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__

    # [END documentation]


    def extract():
        extractor("Google-Cloud").get_data(
            query="SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-01'",
            file_name="us_states_covid19_data.csv"
        )

    def load():
        loader("Supabase").load_data(file_name="us_states_covid19_data.csv",
                                     table='covid19_us_states',
                                     db_reference_id=os.environ['SUPABASE_DB_REFERENCE_ID'],
                                     db_password=os.environ['SUPABASE_DB_PASSWORD']
                                     )

    # [START main_flow]
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> load_task

# [END main_flow]

# [END tutorial]

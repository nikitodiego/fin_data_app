from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime,timedelta
from data.app_functions_optim import api_call,bucket_to_bq
import os
import time

# Define the default_args dictionary
default_args = {
    'owner': 'nikito',
    'start_date': datetime(2023,7,26),
    'end_date': datetime(2023,7,26),
    'retries': 1,
    'schedule_interval':'@daily',
    'depends_on_past' : True,
}

# Create a DAG instance
dag = DAG('ETL_nico_optim_9',
        catchup=True, 
        default_args=default_args,
)

task_1 = PythonOperator(
    task_id='llamada_a_api',
    python_callable=api_call,
    provide_context=True,
    dag=dag,
)

task_2 = PythonOperator(
    task_id='carga_BQ',
    python_callable=bucket_to_bq,
    provide_context=True,
    dag=dag,
)

email = EmailOperator(
    task_id='send_email',
    to='nicojapaz@gmail.com',
    subject='Airflow Alert',
    html_content="Date: {{ ds }} - Value: {{ task_instance.xcom_pull(task_ids='llamada_a_api') }}",
    dag=dag
)

task_1 >> task_2 >> email

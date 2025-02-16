import os
import sys
from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time


PROJECT_ROOT = '/home/wolfframio/Coding/leaderboard/42stats'
sys.path.append(PROJECT_ROOT)

from db_manager import connect_and_get_sample


def get_data(**context):
    result = connect_and_get_sample()
    context['task_instance'].xcom_push(
                                    key='mongo_data',
                                    value=str(result))

email_content="{{ ti.xcom_pull(task_ids='task_get_data', key='mongo_data') }}"


with DAG(
        'test_get_info_from_mongo',
        schedule_interval='* * * * *',
        start_date=datetime(2024, 2, 15),
        catchup=False) as dag:

    task_get_data = PythonOperator(
        task_id='task_get_data',
        python_callable=get_data,
        provide_context=True)

    task_email = EmailOperator(
        task_id='send_email',
        to='estudiosplateau49@gmail.com',
        subject='Report mongo',
        html_content=email_content,
        trigger_rule='all_success'
    )


task_get_data >> task_email

""" result = connect_and_get_sample()
print(result) """
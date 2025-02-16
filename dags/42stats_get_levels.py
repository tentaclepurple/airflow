import logging
import os
import sys
from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time

PROJECT_ROOT = '/home/wolfframio/Coding/leaderboard/42stats'
sys.path.append(PROJECT_ROOT)

from main_get_users_level import init_pipeline


def generate_email_content(**context):
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                text-align: center;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
                margin-bottom: 25px;
                font-size: 24px;
            }}
            .timestamp {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 16px;
                color: #2c3e50;
            }}
            .footer {{
                color: #666;
                font-size: 14px;
                margin-top: 25px;
                border-top: 1px solid #eee;
                padding-top: 15px;
            }}
            strong {{
                color: #34495e;
            }}
            .emoji {{
                font-size: 24px;
                margin-right: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span class="emoji">📊</span>Actualización Base de Datos 42</h1>
            <div class="timestamp">
                <strong>Hora de finalización:</strong><br>
                {execution_time}
            </div>
            <div class="footer">
                <span class="emoji">🚀</span>
                <em>Este mensaje ha sido generado automáticamente por Airflow</em>
            </div>
        </div>
    </body>
    </html>
    """


def wrapped_init_pipeline(**context):
    print("="*50)
    print("DEBUG: Starting pipeline execution")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    print(f"DEBUG: Python path: {sys.path}")
    print(f"DEBUG: Environment variables:")
    for key, value in os.environ.items():
        print(f"  {key}: {value}")
    
    try:
        print("DEBUG: About to call init_pipeline")
        # Verifica que la función existe
        print(f"DEBUG: init_pipeline function: {init_pipeline}")
        result = init_pipeline()
        print(f"DEBUG: Pipeline execution completed with result: {result}")
        return result
    except Exception as e:
        print("="*50)
        print("ERROR DETAILS:")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        print("="*50)
        raise



html_template = """

================================
Task executed at: {{ execution_date.strftime('%Y-%m-%d %H:%M:%S') }}
================================

"""


with DAG(
        '42stats_update_db',
        schedule_interval='0 22 * * *',
        start_date=datetime(2024, 2, 15),
        catchup=False) as dag:

    task_init_email = EmailOperator(
        task_id='send_init_email',
        to='estudiosplateau49@gmail.com',
        subject='42stats fetch data start',
        html_content="""

            ================================
            Task executed at: {{ execution_date.strftime('%Y-%m-%d %H:%M:%S') }}
            ================================

                """)


    task_init_pipeline = PythonOperator(
        task_id='init_pipeline',
        python_callable=wrapped_init_pipeline,
        retries=3,
        retry_delay=timedelta(minutes=30)
    )

    task_end_email = EmailOperator(
        task_id='send_end_email',
        to='estudiosplateau49@gmail.com',
        subject='42stats fetch data end',
        html_content=generate_email_content(),
        trigger_rule='all_success'
        )

task_init_email >> task_init_pipeline >> task_end_email


""" if __name__ == "__main__":
    print("Testing init_pipeline function directly...")
    result = init_pipeline()
    print(f"Result: {result}") """
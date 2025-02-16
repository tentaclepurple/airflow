from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import time

def tarea_prueba(**context):
    tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"La tarea se ejecutó en: {tiempo_actual}\n"
    
    with open('/home/wolfframio/Coding/Airflow/registro_prueba.txt', 'a') as f:
        f.write(mensaje)
    
    # Guardamos el mensaje para el email
    context['task_instance'].xcom_push(key='tiempo_ejecucion', value=mensaje)
    
    time.sleep(10)

# El contenido del email ahora será un template
email_template = """
<h3>Reporte de Ejecución de Tarea</h3>
<p>{{ task_instance.xcom_pull(key='tiempo_ejecucion') }}</p>
<p>Este es un email automático generado por Airflow.</p>
"""

with DAG(
    'prueba_simple',
    schedule_interval='* * * * *',
    start_date=datetime(2024, 2, 15),
    catchup=False
) as dag:

    tarea_archivo = PythonOperator(
        task_id='tarea_archivo',
        python_callable=tarea_prueba,
        provide_context=True
    )

    tarea_email = EmailOperator(
        task_id='enviar_email',
        to='estudiosplateau49@gmail.com',  # Cambia esto por tu correo
        subject='Reporte de Ejecución Airflow',
        html_content=email_template  # Ahora usamos el template
    )

    tarea_archivo >> tarea_email
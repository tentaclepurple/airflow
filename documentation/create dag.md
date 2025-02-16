    nano ~/Coding/Airflow/dags/test.py

<br>

    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from datetime import datetime, timedelta
    import time

    # Esta función es lo que se ejecutará cada minuto
    def tarea_prueba():
        # Guardamos la hora de ejecución en un archivo para poder verificar que funciona
        tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/home/wolfframio/Coding/Airflow/tests/registro_prueba.txt', 'a') as f:
            f.write(f"La tarea se ejecutó en: {tiempo_actual}\n")
        # Esperamos 10 segundos para simular que la tarea hace algo
        time.sleep(10)

    # Configuración básica del DAG
    with DAG(
        'prueba_simple',                     # El nombre que verás en la interfaz
        schedule_interval='* * * * *',       # Se ejecuta cada minuto
        start_date=datetime(2024, 2, 15),    # Desde cuándo empezará
        catchup=False                        # No ejecuta tareas atrasadas
    ) as dag:

        # Definimos nuestra tarea
        tarea = PythonOperator(
            task_id='tarea_test',
            python_callable=tarea_prueba
        )

### dag will be automatically detected if scheduler is up but we need to unpause it

    airflow dags unpause prueba_simple

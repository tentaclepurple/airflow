# New env for Airflow

    conda create -n airflow_env python=3.9

    conda activate airflow_env

Ahora, antes de instalar Airflow, necesitamos configurar dónde queremos que Airflow guarde todos sus archivos. Esto se hace mediante la variable de entorno AIRFLOW_HOME. En tu caso, podríamos usar el directorio actual:



    export AIRFLOW_HOME=/home/wolfframio/Coding/Airflow

    o permanente

    echo 'export AIRFLOW_HOME=/home/wolfframio/Coding/Airflow' >> ~/.bashrc


install airflow

    pip install apache-airflow


Una vez instalado, inicializamos la base de datos de Airflow (por defecto usará SQLite):

    airflow db init

create user admin:

    airflow users create \
    --username admin \
    --firstname tu_nombre \
    --lastname tu_apellido \
    --role Admin \
    --email tu@email.com \
    --password tu_contraseña


start server. Blocks terminal with server logs

    airflow webserver


in another terminal:

    cd /home/wolfframio/Coding/Airflow
    conda activate airflow_env
    airflow scheduler

now open a tunnel to the server to make the airflow webserver accessible via localhost:8080

    ssh -p 42224 -L 8080:localhost:8080 usuario@servidor

